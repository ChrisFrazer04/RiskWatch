from FirstProj.models import Country
import sqlite3

def run():
    conn = sqlite3.connect('C:\\Users\\cflor\\PycharmProjects\\FCC\\WHO_API_DB.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT name, code, population FROM country_migration')
    data = cur.fetchall()
    conn.close()
    for item in data:
        name = item[0]
        code = item[1]
        population = item[2]
        entry = Country(country_name=name, country_code=code, population=population)
        entry.save()
    print(Country.objects.all())
    #conn = sqlite3.connect('C:\\Users\\cflor\\PycharmProjects\\DjangoProject\\db.sqlite3')
    #cur = conn.cursor()


