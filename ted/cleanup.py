import logging
import requests

from sqlalchemy import Unicode
from monnet.ted.util import engine, contracts_table, documents_table


log = logging.getLogger('monnet.ted.cleanup')


def transform():
    documents_table.create_column('year', Unicode)
    engine.query("UPDATE %s SET year = SUBSTR(oj_date, 0, 5)" % documents_table.table.name)

if __name__ == '__main__':
    transform()
