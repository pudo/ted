
all: parse countries cleanup

parse:
	python ted/parse.py

countries:
	python ted/countries.py

cleanup:
	python ted/cleanup.py
