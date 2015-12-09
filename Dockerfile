FROM pudo/scraper-base
MAINTAINER Friedrich Lindenberg <friedrich@pudo.org>

RUN apt-get install -y gdal-bin python-gdal

COPY . /scraper
WORKDIR /scraper
RUN pip install -r requirements.txt
RUN pip install -e .
CMD sh run.sh
