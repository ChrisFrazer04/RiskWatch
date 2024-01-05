import json
import sqlite3
import requests
import time
import csv
import math
import urllib
from GMAPS_API import gapi_request
from bs4 import BeautifulSoup

file = open('C:\\Users\\cflor\\PycharmProjects\\FCC\\country_list.html', mode='r')
soup = BeautifulSoup(file, 'html.parser')
data = soup.find_all('option')

for tag in data:
    tag = str(tag)
    pos1 = tag.find('"')
    ntag = tag[pos1+1:]
    pos2 = ntag.find('"')
    rtag = ntag[:pos2]
    print(rtag)
print(data)
exit()


def write_csv(fieldnames='', rows=''):
    with open('realdata.csv', mode='w') as testsheet:
        writer = csv.DictWriter(testsheet, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        testsheet.close()

def append_csv1(fieldnames='', rows=''):
    with open('testdata.csv', mode='a') as testsheet:
        writer = csv.DictWriter(testsheet, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        testsheet.close()

def append_csv2(data):
    row = dict()
    with open('testdata.csv', mode='r') as testsheet:
        testsheet.readline
        for k,v in data.items():
            row[k] = v
            writer = csv.DictWriter(testsheet, fieldnames=k)
            writer.writeheader()
            writer.writerow(row)
        testsheet.close()


def append_csv3(jsdata):
    rows = list()
    temprows = dict()
    fnames = dict()
    with open('testdata.csv', mode='r') as tsheet:
        l1 = tsheet.readline()
        l1 = l1.strip()
        l2 = l1.split(',')
        for head in l2:
            fnames[head] = 1
        tsheet.close()
    with open('testdata.csv', mode='a') as testsheet:
        for k,v in jsdata.items():
            try:
                k = k.strip()
                dummy = fnames[k]
                continue
            except:
                writer = csv.writer(testsheet)
                temprows[k] = v
                writer.writeheader()
                writer.writerow(temprows)
                temprows = {}
        testsheet.close()

def filter_indicators(tablename, keywords, cat=''):
    if cat == '':
        data = get_data(tablename)
    else:
        data = get_data(tablename, cat)
    id_dict = {}
    count_dict = {}
    count = 1
    for line in data:
        ind_name = line[1]
        ind_id = line[2]
        for keyword in keywords:
            if ind_name.lower().find(keyword.lower()) != -1:
                try:
                    if keyword in id_dict:
                        count_dict[keyword] = 1
                        id_dict[keyword + '_' + str(count_dict[keyword] + 1)] = ind_id
                except:
                    if keyword in id_dict:
                        count_dict[keyword] += 1
                        id_dict[keyword + '_' + str(count_dict[keyword] + 1)] = ind_id
                if keyword not in id_dict:
                    id_dict[keyword] = ind_id
    return id_dict

#Population table creation and insertion
cmd = '''CREATE TABLE population_2021 (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
country TEXT NOT NULL UNIQUE,
population INTEGER NOT NULL)'''
cur.execute(cmd)
with open('Data.csv', mode='r') as data:
    reader = csv.DictReader(data)
    count = 0
    while count < 10:
        for row in reader:
            country = row['ï»¿Data Source']
            population = row['Population']
            cmd = 'INSERT INTO population_2021 (country, population) VALUES ("{}", {})'.format(country, population)
            #pop = row['None']
            #print(pop)
            print(country)
            print(population)
            count +=1

exit()

#Google Maps Code:

bigmaps = gapi_request(False)
bigmaps.make_request(input('Enter Location Here: '))
dta = bigmaps.get_stats()
print(dta['country_data']['long_name'])
exit()
bigmaps.calc_distance(input('Enter Location Here'))
exit()
nmaps = bigmaps.another(False, 'nmaps')
nmaps.make_request('Yale University')
print(nmaps.text)
exit()
bigmaps.make_request('University of Helsinki')
bigmaps.calc_distance('University of Helsinki')
exit()
text = bigmaps.text
js = bigmaps.rawjs
stats = bigmaps.get_stats()
print(stats['country_data'])

exit()









api_key = False
if api_key != False:
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
    api_key = 'AIzaSyAkqT5NcD8JHNfdPqy2iVWqkLDv9Kl208A'
else:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'


address = 'Yale University'
parms = dict()
parms['address'] = address
parms['key'] = api_key
url = serviceurl + urllib.parse.urlencode(parms)
print('Retrieving', url)
file = requests.get(url)
rawjs = file.json()
text = json.dumps(rawjs, indent=4)
print(text)
print(type(file))
exit()
addy_list = ['Yale University']
count = 0
while count < len(addy_list):
    #Parameters/Data Retrieval
    for addy in addy_list:
        count += 1
        address = addy
        if len(address) < 1 or address == 'break':
            break
        parms = dict()
        parms['address'] = address
        parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)
        print('Retrieving', url)
        file = urllib.request.urlopen(url, context=ctx)
        data = file.read().decode()
        print('Retrieved', len(data), 'characters')
    #loading data as JSON
        try:
            js = json.loads(data)
        except:
            js = None
    #Checks to see if data is desired/valid
        if not js or 'status' not in js or js['status'] != 'OK':
            print('=== Failure to Retrieve ===')
            print(data)
            continue
        #json.dump
        print(json.dumps(js, indent=4))
exit()
#Making the database
conn = sqlite3.connect('Maps Database.sqlite')
cur = conn.cursor()
#cur.executescript('DROP TABLE IF EXISTS LocationData')
table_exist = False
cur.execute('DROP TABLE IF EXISTS HospitalLocationData')
if table_exist == False:
    cur.executescript('''
CREATE TABLE HospitalLocationData (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    latitude REAL,
    longitude REAL,
    place_id TEXT UNIQUE,
    address  TEXT UNIQUE
     )''')
    table_exist = True

addy_list = ['Yale University']
count = 0
while count < len(addy_list):
    #Parameters/Data Retrieval
    for addy in addy_list:
        count += 1
        address = addy
        if len(address) < 1 or address == 'break':
            break
        parms = dict()
        parms['address'] = address
        parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)
        print('Retrieving', url)
        response = requests.get(url)
        js = response.json()
        print('Retrieved', len(data), 'characters')
    #loading data as JSON
        try:
            js = json.loads(data)
        except:
            js = None
    #Checks to see if data is desired/valid
        if not js or 'status' not in js or js['status'] != 'OK':
            print('=== Failure to Retrieve ===')
            print(data)
            continue
        #json.dump
        print(json.dumps(js, indent=4))
    #js = whole text. results = first item in js dict which is a list, [0] is the dictionary of all the desired data
        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        place_id = js['results'][0]['place_id']
        name = address
        formatted_address = js['results'][0]['formatted_address']
        cmd = 'INSERT INTO LocationData (name, latitude, longitude, place_id, address) VALUES ("{}", {}, {}, "{}", "{}")'.format(name, lat, lng, place_id, formatted_address)
        cur.execute(cmd)
        conn.commit()
        #print(json.dump(js, indent=4))
        print('latitude: ', lat)
        print('Longitude: ', lng)
        print('Place id: ', place_id)













alright = gapi_request(False)
alright.make_request('Yale University')
print(alright.get_stats())
query = input('What data do you want to see?')
print(alright.get_stats()[query])
exit()
#----------------------------------------------------------------------------------------------------------------------------------------------------
def fetch_country_names_and_ids():
    countries = Table('country_name')
    countries.create_table()
    url = 'https://wits.worldbank.org/wits/wits/witshelp/content/codes/country_codes.htm'
    headers = {'User-agent': 'Mozilla 5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('p', class_='WTNC')
    count = 1
    dict = {}
    pos = 1
    for tag in data:
        if count == 1:
            count = 2
            #cmd = 'INSERT INTO country_name (short_name) VALUES ("{}")'.format(tag.text)
            #countries.execute(cmd)
            dict[pos] = tag.text.strip()
            pos +=1
            continue
        if count == 2:
            count = 1
            continue
    dict2 = {}
    pos = 1
    data2 = soup.find_all('p', class_='WTN')
    for ctr in data2:
        dict2[ctr.text.strip()] = dict[pos]
        pos +=1
    for k,v in dict2.items():
        cmd = 'INSERT INTO country_name (long_name, short_name) VALUES ("{}", "{}")'.format(k, v)
        countries.execute(cmd)
    countries.commit()