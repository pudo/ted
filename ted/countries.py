import logging
# import requests

from ted.util import contracts_table, documents_table


log = logging.getLogger(__name__)


def country_by_name(name):
    # TODO after monnet extract
    return


def transform_prefix(prefix):
    log.info("Normalizing countries for %s...", prefix)
    field = prefix + '_country'
    for row in list(contracts_table.distinct(field)):
        name, code = country_by_name(row.get(field))
        if code is not None:
            row[prefix + '_country_common'] = name
            row[prefix + '_country_code'] = code
            contracts_table.update(row, [field])


def transform():
    #transform_prefix('operator')
    #transform_prefix('authority')

    field = 'iso_country'
    for row in list(documents_table.distinct(field)):
        name, code = country_by_name(row.get(field))
        if code is not None:
            row['country_common'] = name
            documents_table.update(row, [field])


if __name__ == '__main__':
    transform()
