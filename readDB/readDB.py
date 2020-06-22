from flask import Flask
import mysql.connector
import json

app = Flask(__name__)


def readData(chrom, pos, ref, alt):
    # opens the input.txt file for filters
    # input.txt must be a tab-delimited file with the following format:
    # CHROMOSOME (tab) POSITION (tab) REFERENCE ALLELE (tab) ALT ALLELE
    bestand = open("input.txt", "r")
    for line in bestand:
        first = line.split('\n')
        temp = first[0].split('\t')
        chrom.append(temp[0])
        pos.append(int(temp[1]))
        ref.append(temp[2])
        alt.append(temp[3])
    return chrom, pos, ref, alt
    # all filters from input.txt are saved in separate lists, which are passed on to the next function


def processed_data(chrom, pos, ref, alt):
    # connects to the database and pulls all variants matching the filters in input.txt
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'variants'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM processed_data""")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    x = 0
    combo = ""
    while x < len(chrom):
        y = 0
        while y < len(data):
            if chrom[x] == data[y][0]:
                if pos[x] == data[y][1]:
                    if ref[x] == data[y][3]:
                        if alt[x] == data[y][4]:
                            add = data[y][0] + ", " + str(data[y][1]) + ", " + data[y][3] + ", " + data[y][4] + ", " + data[y][5]
                            combo += add
                            combo += "; "
            y += 1
        x += 1
    # first checks for matches in chromosome, then position, then reference allele, and finally alternate allele
    # if all four match, it pulls the data of 'benign/cancer' and adds all five to the printed results

    return combo

@app.route('/')
def index() -> str:
    # runs if the website is opened or refreshed
    chrom = []
    pos = []
    ref = []
    alt = []
    readData(chrom, pos, ref, alt)
    return json.dumps({'Results:': processed_data(chrom, pos, ref, alt)}, separators=(', ',': '))
    # visible output starts with 'Results:' and then prints any variants matching the filters in input.txt
    # the output is formatted like this:
    # CHROMOSOME, POSITION, REFERENCE ALLELE, ALTERNATE ALLELE, BENIGN/CANCER
    # results are separated with a ';'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
