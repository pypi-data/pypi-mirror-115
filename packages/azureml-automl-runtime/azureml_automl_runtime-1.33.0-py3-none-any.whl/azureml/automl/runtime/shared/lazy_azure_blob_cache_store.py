# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module containing the implementation for an azure based cache to be used for saving automl data between runs."""
from typing import Any, Dict, Iterable, List, Optional
import io
import logging
import os
import shutil
import tempfile

import numpy as np
from scipy import sparse

from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.exceptions import CacheException
from azureml.automl.runtime.shared import lazy_file_cache_store
from azureml.data.azure_storage_datastore import AzureBlobDatastore

logger = logging.getLogger()


class LazyAzureBlobCacheStore(lazy_file_cache_store.LazyFileCacheStore):
    """File cache store backed by azure blob."""
    def __init__(
        self,
        data_store: AzureBlobDatastore,
        blob_path: str,
        task_timeout: int = lazy_file_cache_store._CacheConstants.DEFAULT_TASK_TIMEOUT_SECONDS
    ):
        super().__init__(tempfile.mkdtemp())

        self._data_store = data_store
        self._blob_path = blob_path + "/cache"
        self._task_timeout = task_timeout

    def load(self) -> None:
        """
        Read the contents of the blob at the path and store keys, data references to them
        in memory. This will hydrate `cached_items` field of this.
        """
        try:
            blobs = list(self._data_store.blob_service.list_blobs(self._data_store.container_name,
                                                                  prefix=self._blob_path))
        except Exception as ex:
            logging_utilities.log_traceback(ex, logger, is_critical=False)
            msg = "Failed to list blobs in the datastore"
            raise CacheException.from_exception(ex, msg=msg).with_generic_msg(msg)

        for blob in blobs:
            blob_name = blob.name
            cached_file_name = blob_name.split("/")[-1]
            cache_key, ext = self._split_file_ext(cached_file_name)

            if ext == lazy_file_cache_store._CacheConstants.NUMPY_FILE_EXTENSION:
                func = np.load
            elif ext == lazy_file_cache_store._CacheConstants.SCIPY_SPARSE_FILE_EXTENSION:
                func = sparse.load_npz
            else:
                func = self._pickler.load

            self.cache_items[cache_key] = lazy_file_cache_store.CachedValue(blob_name, func)

    def get(self, keys: Iterable[str], default: Optional[Any] = None) -> Dict[str, Any]:
        """
        Get deserialized object from store.

        :param keys: Keys to retrieve the values for.
        :param default: returns default value if not present
        :return: deserialized objects
        """
        Contract.assert_value(value=keys, name='keys', log_safe=True)
        res = {}
        with self.log_activity():
            for key in keys:
                item = self.cache_items.get(key)
                try:
                    if item is not None:
                        in_stream = io.BytesIO()
                        self._data_store.blob_service.get_blob_to_stream(
                            self._data_store.container_name,
                            item.path,
                            in_stream
                        )
                        temp_file = tempfile.NamedTemporaryFile(delete=False)
                        temp_file.write(in_stream.getvalue())
                        temp_file.close()
                        res[key] = item.func(temp_file.name)
                        os.remove(temp_file.name)
                    else:
                        res[key] = default
                except MemoryError:
                    raise
                except Exception as e:
                    logging_utilities.log_traceback(e, logger, is_critical=False)
                    msg = "Failed to retrieve {1} from cache. Exception type: {0}".format(
                        e.__class__.__name__,
                        key)
                    logger.warning(msg)
                    res[key] = default

        return res

    def set(self, key: str, value: Any) -> None:
        """
        Set key and value in the cache.

        :param key: Key to store.
        :param value: Value to store.
        """
        Contract.assert_value(value=key, name='key', log_safe=True)
        self.add([key], [value])

    def add(self, keys: Iterable[str], values: Iterable[Any]) -> None:
        """
        Serialize the values and add them to cache and upload to the azure blob container.

        :param keys: List of keys.
        :param values: Corresponding values to be cached.
        """
        Contract.assert_value(value=keys, name='keys', log_safe=True)
        with self.log_activity():
            try:
                # Write the value temporarily to disk and store refs as
                # CachedValue in self.cache_items.
                # The `path` of the CachedValues is temporary local disk path.
                for key, value in zip(keys, values):
                    self._write(key, value)

                # Upload temp files to blob and return CachedValues with
                # path updated to the uploaded Blob store path.
                uploaded_items = self._upload_multiple([self.cache_items[key] for key in keys])

                # Set the CachedValues back to the index.
                for idx, key in enumerate(keys):
                    self.cache_items[key] = uploaded_items[idx]
            except MemoryError:
                raise
            except Exception as ex:
                logging_utilities.log_traceback(ex, logger, is_critical=False)
                msg = "Failed to add to cache. Exception type: {0}".format(ex.__class__.__name__)
                raise CacheException.from_exception(ex, msg=msg).with_generic_msg(msg)

    def remove(self, key: str) -> None:
        """
        Remove key from store.

        :param key: store key
        """
        try:
            to_remove = self.cache_items[key]
            self._data_store.blob_service.delete_blob(
                self._data_store.container_name,
                to_remove.path,
                timeout=self._task_timeout
            )
            del self.cache_items[key]
        except KeyError as ke:
            logging_utilities.log_traceback(ke, logger, is_critical=False)
            msg = "Failed to find key '{}' in cache.".format(key)
            raise CacheException.from_exception(ke, msg=msg).with_generic_msg(msg)
        except Exception as e:
            logging_utilities.log_traceback(e, logger, is_critical=False)
            msg = "Failed to delete key '{}' from cache. Exception type: {}".format(
                key, e.__class__.__name__)
            raise CacheException.from_exception(e, msg=msg).with_generic_msg(msg)

    def remove_all(self):
        """Remove all the cache from store."""
        keys = list(self.cache_items.keys())
        for key in keys:
            self.remove(key)

    def _upload(self, cached_value: lazy_file_cache_store.CachedValue) -> lazy_file_cache_store.CachedValue:
        """
        Upload a single file represented by cached_value to the blob store.

        :param cached_value: The item to be uploaded.
        :returns: An updated CachedValue with the path pointing to the location of file on blob.
        """
        return self._upload_multiple([cached_value])[0]

    def _upload_multiple(
            self,
            cached_values: List[lazy_file_cache_store.CachedValue]) -> List[lazy_file_cache_store.CachedValue]:
        """
        Upload multiple files represented by cached_values to the blob store.

        :param cached_values: The items to be uploaded.
            NOTE cached_value file paths are not log safe!
        :returns: Updated CachedValue list with the path pointing to the location of files on blob.
        """
        with self.log_activity():
            files = [c.path for c in cached_values]
            file_names = [os.path.split(file_path)[1] for file_path in files]
            upload_path = self._blob_path
            try:
                self._data_store.upload_files(
                    files=files,
                    target_path=upload_path,
                    show_progress=False,
                    overwrite=True
                )
            except MemoryError:
                raise
            except Exception as e:
                logging_utilities.log_traceback(e, logger, is_critical=False)
                msg = "Failed to upload files to the cache. Exception type: {}".format(
                    e.__class__.__name__
                )
                raise CacheException.from_exception(e, msg=msg).with_generic_msg(msg)

            return [lazy_file_cache_store.CachedValue(
                '{upload_path}/{file_name}'.format(upload_path=upload_path, file_name=file_name),
                c.func
            ) for file_name, c in zip(file_names, cached_values)]

    def __repr__(self):
        path = self._blob_path[:self._blob_path.rfind("/cache")]
        return "AzureLazyCacheStore(data_store=\"{}\", blob_path=\"{}\", task_timeout={})".\
            format(self._data_store, path, self._task_timeout)

    def __del__(self):
        shutil.rmtree(self._root)
