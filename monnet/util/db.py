import os
import dataset


DATABASE_URI = os.environ.get('MONNET_ETL_DATABASE')
assert DATABASE_URI, "No database URI defined in MONNET_ETL_DATABASE."

engine = dataset.connect(DATABASE_URI)
