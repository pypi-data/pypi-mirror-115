"""Declares :class:`LocalDiskBackend`."""
import os
import shutil

from .base import BaseStorageBackend


class LocalDiskBackend(BaseStorageBackend):
    """A :class:`~unimatrix.ext.blob.BaseStorageBackend` implementation
    that operates on the local disk(s).
    """
    __module__ = 'unimatrix.ext.blob'
    default_base_path = os.getcwd

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.isabs(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)

    async def download(self, src: str, dst: str, offset: int, length: int):
        """Downloads file from *absolute path* `src` to `dst` on the local
        filesystem.
        """
        if not offset and not length:
            shutil.copy2(src, dst)
            return

        with open(dst, 'wb') as df:
            with open(src, 'rb') as sf:
                sf.seek(offset or 0)
                buf = sf.read(length) if length else sf.read()
                df.write(buf)

    async def exists_internal(self, path: str) -> bool:
        """Test whether an absolute path exists.  Returns False for broken
        symbolic links if the storage backend supports them.
        """
        return os.path.exists(path)

    async def upload(self, src: str, dst: str):
        """Uploads absolute path `src` to absolute path `dst`."""
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        shutil.copy2(src, dst)
