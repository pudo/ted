import logging
import requests

from monnet.util import country_by_name
from monnet.fts.util import engine, fts_entry


log = logging.getLogger(__name__)


def transform():
    log.info("Normalizing countries for FTS recipients...")
    for row in list(fts_entry.distinct('country')):
        name, code = country_by_name(row.get('country'))
        if code is not None:
            row['country_common'] = name
            row['country_code'] = code
            fts_entry.update(row, ['country'])


if __name__ == '__main__':
    transform()
