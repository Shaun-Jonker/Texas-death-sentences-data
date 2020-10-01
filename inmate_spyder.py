import sqlite3
import ssl
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('death_row.sqlite')
cur = conn.cursor()


baseurl = "https://www.tdcj.texas.gov/death_row/dr_offenders_on_dr.html"

cur.execute('''DROP TABLE IF EXISTS inmates''')
conn.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS inmates (id INTEGER PRIMARY KEY, tdcj_number INTEGER, link TEXT, last_name TEXT, 
first_name TEXT, dob TEXT, gender TEXT, race TEXT, date_received TEXT, county TEXT, date_of_offence TEXT)''')

conn.commit()


while True:

    fail = 0

    try:
        # Open with a timeout of 30 seconds
        document = urllib.request.urlopen(baseurl, None, 30, context=ctx)
        text = document.read().decode()
        if document.getcode() != 200:
            print("Error code=", document.getcode(), baseurl)
            break
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page", baseurl)
        print("Error", e)
        fail = fail + 1
        if fail > 5:
            break
        continue

    soup = BeautifulSoup(text, 'html.parser')
    tags = soup('tr')

    tds = list()
    for tr in soup.find_all('tr'):
        tds.append(tr.find_all('td'))

    for td in tds[1:]:
        tdcj_number = td[0].text
        link = 'https://www.tdcj.texas.gov/death_row/' + str(td[1].find('a', href=True)['href'])
        lastname = td[2].text
        firstname = td[3].text
        dob = td[4].text
        gender = td[5].text
        race = td[6].text
        date_received = td[7].text
        county = td[8].text
        date_of_offence = td[9].text
        cur.execute('''INSERT OR IGNORE INTO inmates (tdcj_number, link, last_name, first_name, dob, gender, race, 
                date_received, county, date_of_offence) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
                    (tdcj_number, link, lastname, firstname, dob, gender, race, date_received, county, date_of_offence))
        conn.commit()

    break
