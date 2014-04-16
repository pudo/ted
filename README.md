# Monnet

This package contains a set of Python scrapers for data sources related to the European Union. In particular, in contains the following data extractors:

* ``monnet/experts`` - EC/EP Register of Expert Groups, i.e. data about the structure and membership of EU advisory bodies on a variety of topics.
* ``monnet/fts`` - EC Financial Transparency System, i.e. direct expenditures of the European Commission.
* ``monnet/interests`` - EC/ECP Register of Interests, i.e. the EU's lobby register (such as it is). Includes companies, think tanks and NGOs which lobby the Commission or Parliament. Includes EP accredditation data.
* ``monnet/ted`` - Tenders Electronic Daily, the EU's joint procurement system. This includes tenders and contract awards not just for EU bodies, but also the member states.

The data is collected and aggregated in a SQL database, with each data sources tables prefixed with an identifier.

## Configuration

The configuration of ``monnet`` is handled via a set of environment variables that must be set before any of the ETL scripts can be executed:

* ``MONNET_DATA_PATH`` - the main storage location for data acquired by ``monnet``. If you wish to scrape TED, this folder should be able to hold several gigabytes of data.
* ``MONNET_ETL_DATABASE`` - a SQLAlchemy database URI for the ETL database. While any backend should work, Postgres is recommended. Examples: ``postgresql://user:password@localhost/monnet``.
* ``ECAS_USER`` and ``ECAS_PASSWORD`` are expected to be credentials for the [European Commission Authentication Service](http://ec.europa.eu/europeaid/work/onlineservices/pador/register_en.htm) used by the TED scraper. Sign-up is free.
* ``OPENEXCHANGERATES_APPID`` is a key for the [Open Exchange Rates](https://openexchangerates.org/) API that can be used to perform currency conversions at specific points in time.
* ``NOMENKLATURA_HOST`` and ``NOMENKLATURA_APIKEY`` set access parameters for the API of [OpenNames.org](http://opennames.org) which is used to harmonize country names used in the different datasets.

## Usage

The commands used to run the scrapers in ``monnet`` are encapsulated in the included ``Makefile``, so a basic installation and usage would look like this:

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python setup.py develop
```

This concludes the installation, after setting the environment variables given above and making sure the database exists, you can run the scrapers:

```bash
$ make
# more specific:
$ make ted
```

For more details on the available targets, read the ``Makefile``.
