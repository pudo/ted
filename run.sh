if [ -z "$DATA_PATH" ]; then
    echo "Need to set DATA_PATH"
    exit 1
fi

URL=ftp://guest:guest@ted.europa.eu/daily-packages/

DATA_PATH=$DATA_PATH/ted
SOURCE_PATH=$DATA_PATH/sources
mkdir -p $SOURCE_PATH
wget -c -t 5 -nc -nH -P $SOURCE_PATH -r -l 5 --cut-dirs 1 --accept .tar.gz $URL

python ted_2012_2015/parse.py
