import logging
# import requests

from sqlalchemy import Unicode
from ted.util import engine, documents_table


log = logging.getLogger(__name__)


def transform():
    documents_table.create_column('year', Unicode)
    q = "UPDATE %s SET year = SUBSTR(oj_date, 0, 5)"
    engine.query(q % documents_table.table.name)

if __name__ == '__main__':
    transform()
