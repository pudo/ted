import logging
from monnet.util.db import engine
from monnet.util.cache import fetch_data, walk_path
from monnet.util.geocode import geocode
from monnet.util.countries import country_by_name

logging.basicConfig(level=logging.DEBUG)

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

alembic_log = logging.getLogger("alembic")
alembic_log.setLevel(logging.WARNING)

dataset_log = logging.getLogger("dataset")
dataset_log.setLevel(logging.WARNING)
