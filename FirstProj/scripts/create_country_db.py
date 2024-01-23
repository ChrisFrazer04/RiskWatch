from FirstProj.models import Country
import sqlite3
import pandas as pd
import os

def insert_row(row):
    """Inserts the data from each dataframe row into the Country model/DB"""
    item = Country(country_name=row['country_name'], country_code=row['country_code'],
                   pop2020=row['pop2020'], pop2021=row['pop2021'], pop2022=row['pop2022'])
    item.save()
    print(Country.objects.all())
def run():
    """Points to the data csv file and runs insert_row"""
    data = pd.read_csv('C:\\Users\\cflor\\PycharmProjects\\RiskWatch\\Spreadsheets\\pop_2020-2022.csv')
    data.apply(insert_row, axis=1)
    #print(Country.objects.all())



