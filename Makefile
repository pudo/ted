
all: download parse countries cleanup

download:
	python monnet/ted/download.py

parse:
	python monnet/ted/parse.py

iso-list:
	python monnet/ted/iso_list.py

isos: ted-iso-list
	sh scripts/update-ted.sh

countries:
	python monnet/ted/countries.py

cleanup:
	python monnet/ted/cleanup.py
