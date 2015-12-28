from slugify import slugify
import csv

reader = csv.reader(open("2009.csv"))

with open("2009-wslugs.csv", "wb") as csvfile:
    writer = csv.writer(csvfile)
    
    
    for n,row in enumerate(reader):

        if n == 0:
            writer.writerow(row)

    
        elif row[19] != "procuringEntity/x_slug":
            row[19] = slugify(row[18])
            row[41] = slugify(row[40])

            writer.writerow(row)

