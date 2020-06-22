import re
import mysql.connector
from flask import Flask

app = Flask(__name__)

def readData(val):
    # opens a .vcf file from gnomAD with variant data
    # to replace the file, add the desired .vcf file in the same format to the 'fillDB' folder,
    # and change its name in the 'fillDB' dockerfile and in the line below
    bestand = open("gnomad.exomes.r2.1.1.sites.13.vcf", "r")
    countInfo = 0
    delet = []

    for line in bestand:
        # reads the variant data
        regData = re.findall("^[0-9]|^[YX]", line)
        if regData:
            # if the line starts with any number, or X or Y, it must be a variant listing its chromosome
            temp = line.split('\t')
            val.append((temp[0],temp[1],temp[2],temp[3],temp[4]))

        regInfo = re.findall("^##INFO=", line)
        if regInfo:
            # reads the info to find "non_cancer"
            regTwo = re.findall("^##INFO=<ID=non_cancer_", line)
            if regTwo:
                delet.append(countInfo)
            countInfo += 1
    for x in val:
        # if the entry matches with one marked as non_cancer by the previous function it is marked as benign.
        # all other entries are marked as cancer
        # this functionality lacks the filtering for variants that occur in <1% of population;
        # due to lack of time and storage space I was unable to work with the full-size files
        # which in turn prevented me from figuring out how to achieve such filtering
        y = val.index(x)
        prep = val[y]
        listed = list(prep)
        if y in delet:
            listed.append('benign')
            prep = tuple(listed)
            val[y] = prep
        else:
            listed.append('cancer')
            prep = tuple(listed)
            val[y] = prep

    return val
    # returns all data, formatted in the correct manner to insert into the database


def fillDB(val):
    # takes the data gathered in readData() and inserts it into the mySQL database
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'variants'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    sql = 'INSERT INTO processed_data(chromosome, position, id, changeFrom, changeTo, cancer) VALUES (%s, %s, %s, %s, %s, %s)'
    cursor.executemany(sql, val)
    connection.commit()
    cursor.close()
    connection.close()
    return val
    # this function keeps giving me trouble so if it doesn't work... I really don't know what's up with it
    # when I tested it earlier it worked fine, but when I tried running the entire script it suddenly stopped
    # not even switching it back to the way that worked earlier fixed it
    # just said it couldn't connect to the SQL database
    # so I haven't been able to test the insertion of actual data BUT theoretically it should work


def main():
    val = []
    readData(val)
    fillDB(val)


main()