
all: parse countries cleanup

parse:
	python monnet/ted/parse.py

countries:
	python monnet/ted/countries.py

cleanup:
	python monnet/ted/cleanup.py
