import os
import logging
import tarfile

from ted.util import DATA_PATH

log = logging.getLogger(__name__)


def ted_documents():
    sources_path = os.path.join(DATA_PATH, 'sources')
    log.info('Loading XML bundles (.tar.gz) from %r', sources_path)
    for (dirpath, dirnames, filenames) in os.walk(sources_path):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if not tarfile.is_tarfile(path):
                continue
            log.info('Loading: %r', path)
            with tarfile.open(path) as tar:
                for member in tar.getmembers():
                    if not member.name.endswith('.xml'):
                        continue
                    fh = tar.extractfile(member)
                    yield member.name, fh.read()
