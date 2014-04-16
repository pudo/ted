
all: fts experts ted interests

env:
	@echo "Monnet 0.1"

####################################################
# EC Financial Transparency System

fts-download: env
	python monnet/fts/download.py

fts-parse: env
	python monnet/fts/parse.py

fts-geocode: env
	python monnet/fts/geocode.py

fts-countries: env
	python monnet/fts/countries.py

fts: fts-download fts-parse fts-countries fts-geocode


####################################################
# EC/EP Expert Groups

experts-download: env
	python monnet/experts/download.py

experts-parse: env
	python monnet/experts/parse.py

experts-countries: env
	python monnet/experts/countries.py

experts: experts-download experts-parse experts-countries


####################################################
# Tenders Electronic Daily

ted-download: env
	python monnet/ted/download.py

ted-parse: env
	python monnet/ted/parse.py

ted-iso-list: env
	python monnet/ted/iso_list.py

ted-isos: ted-iso-list
	sh scripts/update-ted.sh

ted-countries:
	python monnet/ted/countries.py

ted: ted-download ted-parse ted-countries


####################################################
# EC/EP Register of Interests

interests-parse: env
	python monnet/interests/parse_interests.py

accredditations-parse: env
	python monnet/interests/parse_accredit.py

interests-categories: env
	python monnet/interests/categories.py

interests-geocode: env
	python monnet/interests/geocode.py

interests-countries: env
	python monnet/interests/countries.py

interests: interests-parse accredditations-parse interests-categories interests-countries interests-geocode

