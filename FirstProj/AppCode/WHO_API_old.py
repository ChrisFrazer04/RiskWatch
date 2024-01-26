import json
import sqlite3
import requests
import time
import csv
import math
import urllib
#from GMAPS_API import gapi_request
#from bs4 import BeautifulSoup


#global cstrlist
#cstrlist = list()
class api_request:
    def __init__(self, serviceRoot='', addon='', params='', headers=''):
        self.serviceRoot = serviceRoot
        if addon == '':
            self.addon = ''
        self.addon = addon
        self.params = params
        if params == '':
            self.params = ''
        self.headers = headers
        if headers == '':
            self.headers = ''
        self.url = self.serviceRoot + self.addon + self.params + self.headers

    def get_url(self):
        url = self.serviceRoot + self.addon + self.params + self.headers
        return url

    def set_serviceRoot(self, serviceRoot):
        self.serviceRoot = serviceRoot
        return serviceRoot

    def set_headers(self, headers={}):
        self.headers = headers
        return headers

    def set_params(self, params):
        self.params = params
        return params

    def set_addon(self, addon):
        self.addon = addon
        return addon

    def make_request(self):
        url = self.get_url()
        self.response = requests.get(url)
        if self.response.status_code != 200:
            print('Error')
            print(self.response.text)
            exit()
        self.rawjs = self.response.json()
        self.text = json.dumps(self.rawjs, indent=4)
        self.status = self.response.status_code

    def err_check(self):
        if self.response.status_code != 200:
            print('Error')
            exit()
            print(self.text)
            exit()
            return self.text
        else:
            print('Successfully connected')

    def get_text_file(self):
        fh = open('C:\\Users\\cflor\\PycharmProjects\\FCC\\BigTest.txt')
        file = fh.read()
        text = json.loads(file)
        values = text['value']
        return text

    def get_indicators(self):
        t = 'in progress'

class sql_req(api_request):
    def __init__(self):
        self.connect()
    def connect(self, name=''):
        if name == '':
            global conn
            conn = sqlite3.connect('C:\\Users\\cflor\\PycharmProjects\\FCC\\WHO_API_DB.sqlite')
            #conn = sqlite3.connect(input('Input Database file') + '.sqlite')
            global cur
            self.cur = conn.cursor()
            cur = self.cur
        else:
            conn = sqlite3.connect(input('Input Database file') + '.sqlite')
            self.cur = conn.cursor()
            cur = self.cur

class Table(sql_req):
    def __init__(self, name='', created=1, columns=[],):
        if name == '':
            self.name = input('Insert table name: ')
        else:
            self.name = name
        self.connect()

    def create_table(self,option=''):
        name = self.name
        ncmd = 'DROP TABLE IF EXISTS {}'.format(name)
        cur.execute(ncmd)
        self.columns = list()
        self.names = list()
        self.names.append(name)
        command = ''
        self.catstr = ''
        #Change the if ___ to a while True statement to return back to inputs
        if option.lower() == 'indicator':
            self.ind_tbl_create()
            self.write_catstr()
            return
        while True:
            query = input('Insert column name and parameters (TEXT, UNIQUE, PRIMARY KEY, etc.). Insert "Done" when finished.')
            if query.lower() == 'done':
                break
            self.columns.append(query)
            command += '{}, '.format(query)
            split = query.split()
            cat = split[0]
            if cat == 'id':
                continue
            self.catstr += '{}, '.format(cat)
        self.catstr = self.catstr[:-2]
        command = command[:-2]
        cmd = "CREATE TABLE {} ({})".format(name, command)
        cur.execute(cmd)
        cstrtxt = '{}:{}'.format(self.name, self.catstr)
        cstrlist.append(cstrtxt)
        self.write_catstr()
        return

    def write_catstr(self):
        fh = open('C:\\Users\\cflor\\PycharmProjects\\FCC\\DB catstr.txt', 'a')
        with fh as f:
            for l in cstrlist:
                f.write(l)
                f.write('\n')
        f.close()

    def ind_tbl_create(self):
        cmd = '''CREATE TABLE {} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name TEXT ,
                    IndicatorCode TEXT UNIQUE)'''.format(self.name)
        cur.execute(cmd)
        #cstrtxt = '{}:name, IndicatorCode'.format(self.name)
        #cstrlist.append(cstrtxt)
    def execute(self, comm):
        cur.execute(comm)
        return

    def commit(self):
        conn.commit()
        return

    def show_stats(self):
        print(self.names)
        print(self.columns)

    def insert(self, colstr, value1, value2):
        name = self.name
        cmd = 'INSERT INTO {} ({}) VALUES ("{}", "{}")'.format(self.name, colstr, value1, value2)
        self.execute(cmd)
        return

    def select(self, arg):
        cmd = 'SELECT {} FROM {}'.format(arg, self.name)
        selected = cur.execute(cmd)
        return selected

def cleansql_str(arg):
    dlist = list()
    for line in arg:
        line = str(line)
        clean1 = line.find("'")
        nline = line[clean1 + 1:]
        clean2 = nline.find("'")
        indicator = nline[:clean2]
        dlist.append(indicator)
        #print(indicator)
    return dlist
def cleansql_int(arg):
    dlist = list()
    for line in arg:
        line = str(line)
        clean1 = line.find("(")
        nline = line[clean1 + 1:]
        clean2 = nline.find(",")
        indicator = nline[:clean2]
        indicator = int(indicator)
        dlist.append(indicator)
        #print(indicator)
    return dlist

def get_columns(tablename):
    fh = open('C:\\Users\\cflor\\PycharmProjects\\FCC\\DB catstr.txt', 'r')
    file = fh.read()
    sp1 = file.split('\n')
    tablename = tablename.lower()
    for line in sp1:
        line = line.lower()
        if line.find('{}'.format(tablename)) != -1:
            sp2 = line.split(':')
            rcstr = sp2[1]
            return rcstr
        else:
            continue

#Input a list of diseases and this function creates a database of indicator codes and indicator names
def create_indicator_DB(disease_list):
    if type(disease_list) == str:
        disease_list = [disease_list]
    for disease in disease_list:
        disease = disease.lower()
        ODATA_API = api_request('https://ghoapi.azureedge.net/api/')
        ODATA_API.set_addon("Indicator?$filter=contains(IndicatorName, '{}')".format(disease))
        ODATA_API.make_request()
        text = ODATA_API.rawjs
        ODATA_API.err_check()
        SQL_DB = sql_req()
        tbl1 = Table(disease)
        tbl1.create_table('indicator')
        values = text['value']
        for line in values:
            Ind_name = line['IndicatorName']
            Ind_code = line['IndicatorCode']
            cmd = 'INSERT INTO {} ({}) VALUES ("{}", "{}")'.format(tbl1.name, get_columns(disease), Ind_name,
                                                                   Ind_code)
            cur.execute(cmd)
        conn.commit()
        time.sleep(0.2)
    return

#Idea to add onto this: add a text input to filter through/choose a certain indicator in the function arguments
def get_data(tablename, column=''):
    if column == '':
        categories = 'id, {}'.format(get_columns(tablename))
    else:
        categories = 'id, {}'.format(column)
    cur.execute('SELECT {} FROM {}'.format(categories, tablename))
    data = cur.fetchall()
    return data

def filter_indicators(tablename, keywords, cat=''):
    if cat == '':
        data = get_data(tablename)
    else:
        data = get_data(tablename, cat)
    id_dict = {}
    for line in data:
        ind_name = line[1]
        ind_id = line[2]
        for keyword in keywords:
            if ind_name.lower().find(keyword.lower()) != -1:
                if ind_id in id_dict.keys():
                    continue
                if ind_id not in id_dict.keys():
                    id_dict[ind_id] = keyword
    return id_dict

def filter_indicators_2(tablename, keyword, returned_columns, filtered_column):
    cmd = 'SELECT {} FROM {} WHERE instr({}, "{}") > 0'.format(returned_columns, tablename, filtered_column, keyword)
    cur.execute(cmd)
    lst = cur.fetchall()
    return(lst[0])

def country_name_to_id(country):
    tup = filter_indicators_2(tablename='country_name', keyword=country, returned_columns='long_name, short_name', filtered_column='long_name')
    id = tup[1]
    return id



def id_to_name(id, tablename):
    if tablename == 'country_name':
        tup = filter_indicators_2(tablename=tablename, keyword=id, returned_columns='long_name',
                                  filtered_column='short_name')
        name = tup[0]
    else:
        tup = filter_indicators_2(tablename=tablename, keyword=id, returned_columns='name', filtered_column='IndicatorCode')
        name = tup[0]
    return name

def check_table(disease):
    try:
        cmd = 'SELECT * FROM {}'.format(disease)
        cur.execute(cmd)
        print('{} Table Exists'.format(disease))
        return
    except:
        create_indicator_DB(disease)
        li = '{} created'.format(disease)
        print(li)
        return

def get_data_specific(countries='', keywords='', diseases='', year=''):
    if type(countries) == str:
        country = countries.lower()
        countries = [countries]
    count = 0
    for country in countries:
        count +=1
        print('loading...' + ' ' + str(count) + '/259')
        if diseases == '':
            diseases = []
            while True:
                dis = input('Enter Disease Here:')
                if dis.lower() == 'done':
                    break
                diseases.append(dis)
        if type(diseases) == str:
            diseases = [diseases]
        keyword_list = []
        if keywords == 'custom':
            while True:
                keyword = input('Enter Keyword:')
                if keyword.lower() == 'done':
                    break
                keyword_list.append(keyword)
            keywords = keyword_list
        else:
            keywords = ['Usable']
        if year == '':
            year = 2021
        country_id = country_name_to_id(country)
        for disease in diseases:
            disease = disease.lower()
            check_table(disease)
            check_data_presence(disease)
            check = check_data_table(disease, country)
            if check != False:
                break
            keyword_list = filter_indicators_2(tablename=disease, keyword='Usable', filtered_column='name', returned_columns='name, IndicatorCode')
            values_dict = {}
            indicator_code = keyword_list[1]
            api_req = api_request(indicator_code)
            api_req.set_serviceRoot('https://ghoapi.azureedge.net/api/')
            query = "?$filter= TimeDim eq {} and SpatialDim eq '{}'".format(str(year), country_id)
            addon = indicator_code + query
            api_req.set_addon(addon)
            api_req.make_request()
            data = api_req.rawjs
            print(data)
            tname = id_to_name(indicator_code, disease)
            name = '{}_{}'.format(country, tname)
            useful_data = data['value']
            if useful_data == []:
                time.sleep(0.1)
                break
            useful_data = data['value'][0]
            #print(useful_data)
            #print(type(useful_data))
            values_dict['cases'] = useful_data['Value']
            #print(type(values_dict['cases']))
            if type(values_dict['cases']) != int:
                time.sleep(0.1)
                break
            values_dict['year'] = useful_data['TimeDim']
            values_dict['population'] = get_population(country)
            mod = values_dict['population'] / 1000
            try:
                values_dict['cases'] = useful_data['NumericValue']
                values_dict['incidence'] = (values_dict['cases']/mod)
            except:
                values_dict['incidence'] = (values_dict['cases']/mod)
            create_sql_data_tbl(disease)
            values_dict['name'] = name
            cmd = 'INSERT INTO {}_data (name, cases, population, incidence, year) VALUES ("{}", {}, {}, {}, {})'.format(disease, name, values_dict['cases'], values_dict['population'], values_dict['incidence'], year)
            cur.execute(cmd)
            conn.commit()
            time.sleep(0.3)
    return values_dict

def check_data_table(disease, country):
    disease +='_data'
    try:
        cmd = 'SELECT * FROM {} WHERE name LIKE "%{}%"'.format(disease, country)
        cur.execute(cmd)
        text = cur.fetchall()
        values_dict = {}
        values_dict['name'] = text[0][1]
        values_dict['cases'] = text[0][2]
        values_dict['year'] = text[0][5]
        values_dict['population'] = text[0][3]
        values_dict['incidence'] = text[0][4]
        return values_dict
    except:
        return False



def append_csv(jsdata):
    all_fieldnames = jsdata.keys()
    fn = dict()
    exist_list = list()
    with open('realdata2.csv', mode='r') as testsheet:
        l1 = testsheet.readline()
        l1 = l1.strip()
        l2 = l1.split(',')
        for head in l2:
            exist_list.append(head)
            fn[head] = 1
        testsheet.close()
    for header in all_fieldnames:
        try:
            exist_list.index(header)
            jsdata.pop(header)
        except:
            continue

def append_csv1(fieldnames='', rows=''):
    with open('testdata.csv', mode='a') as testsheet:
        writer = csv.DictWriter(testsheet, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        testsheet.close()

def create_sql_data_tbl(disease):
    disease = disease.lower()
    disease +='_data'
    try:
        cmd = 'SELECT * FROM {}'.format(disease)
        cur.execute(cmd)
        print('{} Table Exists'.format(disease))
        return True
    except:
        cmd2 = '''CREATE TABLE {} (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        cases FLOAT NOT NULL,
        population INTEGER NOT NULL,
        incidence FLOAT INTEGER NOT NULL,
        year INTEGER NOT NULL
        )'''.format(disease)
        cur.execute(cmd2)
        print('{} Table Created'.format(disease))

def insert_sql_data_tbl(rawjs, disease):
    create_sql_data_tbl(disease=disease)
    disease +='_data'
    for k,v in rawjs.items():
        cmd = '''INSERT INTO {} ({}) VALUES ({}, {})'''.format(disease, get_columns(disease), k, v)
        cur.execute(cmd)
    conn.commit()

def create_presence_table():
    cmd = '''CREATE TABLE data_presence (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL Unique,
    cases TEXT NOT NULL,
    deaths TEXT NOT NULL,
    incidence TEXT NOT NULL,
    mortality TEXT NOT NULL,
    endemicity TEXT NOT NULL)'''
    cur.execute(cmd)
def create_population_table():
    sql_req()
    cmd = '''CREATE TABLE population_2021 (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL UNIQUE,
    population INTEGER NOT NULL)'''
    cur.execute(cmd)
def check_data_presence(tablename):
    try:
        cur.execute('SELECT name FROM data_presence')
        txt = cur.fetchall()
        for lin in txt:
            lin = str(lin)
            if lin.find(tablename) != -1:
                return
    except:
        create_presence_table()
    cmd = 'SELECT name FROM {}'.format(tablename)
    cur.execute(cmd)
    text = cur.fetchall()
    mortality = 'N'
    cases = 'N'
    incidence = 'N'
    death = 'N'
    endemic = 'N'
    for line in text:
        line = str(line)
        rline = line[1:-2]
        if line.find('cases') != -1:
            cases = 'Y'
        if line.find('death') != -1:
            death = 'Y'
        if line.find('incidence') != -1:
            incidence = 'Y'
        if line.find('mortality') != -1:
            mortality = 'Y'
        if line.find('endemic') != -1:
            endemic = 'Y'
    cmd2 = 'INSERT INTO data_presence (name, cases, deaths, incidence, mortality, endemicity) VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'.format(tablename, cases, death, incidence, mortality, endemic)
    cur.execute(cmd2)
    conn.commit()

def initiate(address, keywords='', diseases='', year=''):
    if diseases == '':
        diseases = []
        while True:
            dis = input('Enter Disease Here:')
            if dis.lower() == 'done':
                break
            diseases.append(dis)
    if type(diseases) == str:
        diseases = [diseases]
    if keywords == 'custom':
        keyword_list = []
        while True:
            keyword = input('Enter Keyword:')
            if keyword.lower() == 'done':
                break
            keyword_list.append(keyword)
        keywords = keyword_list
    else:
        keywords = ['cases']
    if year == '':
        year = 2021
    gmaps = gapi_request(True)
    gmaps.make_request_gmaps(address)
    stats = gmaps.get_stats()
    country = stats['country_data']['long_name']
    result_dict = {}
    values = get_data_specific(country=country, keywords=keywords, diseases=diseases, year=year)
    gmaps.search_nearby(location=address, radius_meters=2000, type='hospital')
    print(gmaps.nearby_js)
    hospital_count = 0
    for hospital in gmaps.nearby_js['results']:
        hospital_count += 1
    density = hospital_count / 2
    result_dict['hospital_density'] = density
    result_dict['case_rate'] = values['NumericValue'] / get_population(country)

    return result_dict
    exit()
    #API calls for medim and large radius searches. Activate when ready
    mid_radius = gmaps.search_nearby(location=address, radius_meters=4000, type='hospital')
    hospital_count = 0
    for hospital in gmaps.nearby_js['results']:
        hospital_count += 1
    density = hospital_count / 4
    density_dict['medium_radius'] = density
    large_radius = gmaps.search_nearby(location=address, radius_meters=6000, type='hospital')
    hospital_count = 0
    for hospital in gmaps.nearby_js['results']:
        hospital_count += 1
    density = hospital_count / 6
    density_dict['large_radius'] = density

def get_population(country):
    cmd = 'SELECT population FROM population_2021 WHERE country="{}"'.format(country)
    cur.execute(cmd)
    text = cur.fetchall()
    return text[0][0]

def get_min_max(disease):
    cmd = 'SELECT incidence FROM {}_data'.format(disease)
    cur.execute(cmd)
    biglist = []
    nums = cur.fetchall()
    for num in nums:
        biglist.append(num[0])
    print(biglist)
    mx = max(biglist)
    mn = min(biglist)
    print(mx)
    print(mn)