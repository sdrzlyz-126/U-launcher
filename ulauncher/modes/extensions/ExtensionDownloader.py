import os
import logging
import tarfile
from urllib.request import urlretrieve
from tempfile import mktemp, mkdtemp
from shutil import rmtree, move
from datetime import datetime
from ulauncher.utils.mypy_extensions import TypedDict

from ulauncher.config import EXTENSIONS_DIR
from ulauncher.utils.decorator.singleton import singleton
from ulauncher.api.shared.errors import UlauncherAPIError, ExtensionError
from ulauncher.modes.extensions.ExtensionDb import ExtensionDb, ExtensionRecord
from ulauncher.modes.extensions.ExtensionRemote import ExtensionRemote


logger = logging.getLogger()


class ExtensionDownloaderError(UlauncherAPIError):
    pass


class ExtensionIsUpToDateError(Exception):
    pass


LastCommit = TypedDict('LastCommit', {
    'last_commit': str,
    'last_commit_time': str
})


class ExtensionDownloader:

    @classmethod
    @singleton
    def get_instance(cls) -> 'ExtensionDownloader':
        ext_db = ExtensionDb.get_instance()
        return cls(ext_db)

    def __init__(self, ext_db: ExtensionDb):
        super().__init__()
        self.ext_db = ext_db

    def download(self, url: str) -> str:
        """
        1. check if ext already exists
        2. get last commit info
        3. download & untar
        4. add it to the db

        :rtype: str
        :returns: Extension ID
        :raises AlreadyDownloadedError:
        """
        remote = ExtensionRemote(url)

        # 1. check if ext already exists
        ext_path = os.path.join(EXTENSIONS_DIR, remote.extension_id)
        # allow user to re-download an extension if it's not running
        # most likely it has some problems with manifest file if it's not running
        if os.path.exists(ext_path):
            raise ExtensionDownloaderError(
                f'Extension with URL "{url}" is already added',
                ExtensionError.AlreadyAdded
            )

        # 2. get last commit info
        commit_sha, commit_time = remote.get_latest_compatible_commit()

        # 3. download & untar
        filename = download_tarball(remote.get_download_url(commit_sha))
        untar(filename, ext_path)

        # 4. add to the db
        self.ext_db.put(remote.extension_id, {
            'id': remote.extension_id,
            'url': url,
            'updated_at': datetime.now().isoformat(),
            'last_commit': commit_sha,
            'last_commit_time': commit_time.isoformat()
        })
        self.ext_db.commit()

        return remote.extension_id

    def remove(self, ext_id: str) -> None:
        rmtree(os.path.join(EXTENSIONS_DIR, ext_id))
        self.ext_db.remove(ext_id)
        self.ext_db.commit()

    def update(self, ext_id: str) -> bool:
        """
        :raises ExtensionDownloaderError:
        :rtype: boolean
        :returns: False if already up-to-date, True if was updated
        """
        commit = self.get_new_version(ext_id)
        ext = self._find_extension(ext_id)

        logger.info('Updating extension "%s" from commit %s to %s', ext_id,
                    ext['last_commit'][:8], commit['last_commit'][:8])

        ext_path = os.path.join(EXTENSIONS_DIR, ext_id)

        remote = ExtensionRemote(ext['url'])
        filename = download_tarball(remote.get_download_url(commit['last_commit']))
        untar(filename, ext_path)

        ext['updated_at'] = datetime.now().isoformat()
        ext['last_commit'] = commit['last_commit']
        ext['last_commit_time'] = commit['last_commit_time']
        self.ext_db.put(ext_id, ext)
        self.ext_db.commit()

        return True

    def get_new_version(self, ext_id: str) -> LastCommit:
        """
        Returns dict with commit info about a new version or raises ExtensionIsUpToDateError
        """
        ext = self._find_extension(ext_id)
        url = ext['url']
        remote = ExtensionRemote(url)
        commit_sha, commit_time = remote.get_latest_compatible_commit()
        need_update = ext['last_commit'] != commit_sha
        if not need_update:
            raise ExtensionIsUpToDateError('Extension is up to date')

        return {
            'last_commit': commit_sha,
            'last_commit_time': commit_time.isoformat()
        }

    def _find_extension(self, ext_id: str) -> ExtensionRecord:
        ext = self.ext_db.find(ext_id)
        if not ext:
            raise ExtensionDownloaderError("Extension not found", ExtensionError.Other)
        return ext


def untar(filename: str, ext_path: str) -> None:
    """
    1. Remove ext_path
    2. Extract tar into temp dir
    3. Move contents of <temp_dir>/<project_name>-master/* to ext_path
    """
    if os.path.exists(ext_path):
        rmtree(ext_path)

    temp_ext_path = mkdtemp(prefix='ulauncher_dl_')

    with tarfile.open(filename, mode="r") as archive:
        archive.extractall(temp_ext_path)

    for dir in os.listdir(temp_ext_path):
        move(os.path.join(temp_ext_path, dir), ext_path)
        # there is only one directory here, so return immediately
        return


def download_tarball(url: str) -> str:
    dest_tar = mktemp('.tar.gz', prefix='ulauncher_dl_')
    filename, _ = urlretrieve(url, dest_tar)

    return filename
