# Monnet

This package contains a set of Python scrapers for data sources related to the European Union. In particular, in contains the following data extractors:

* ``monnet/experts`` - EC/EP Register of Expert Groups, i.e. data about the structure and membership of EU advisory bodies on a variety of topics.
* ``monnet/fts`` - EC Financial Transparency System, i.e. direct expenditures of the European Commission.
* ``monnet/interests`` - EC/ECP Register of Interests, i.e. the EU's lobby register (such as it is). Includes companies, think tanks and NGOs which lobby the Commission or Parliament. Includes EP accredditation data.
* ``monnet/ted`` - Tenders Electronic Daily, the EU's joint procurement system. This includes tenders and contract awards not just for EU bodies, but also the member states.

The data is collected and aggregated in a SQL database, with each data sources tables prefixed with an identifier.

## Configuration

ECAS_USER
ECAS_PASSWORD

MONNET_DATA_PATH
MONNET_ETL_DATABASE

OPENEXCHANGERATES_APPID

NOMENKLATURA_HOST
NOMENKLATURA_APIKEY
