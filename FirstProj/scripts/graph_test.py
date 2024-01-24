from django_pandas.io import read_frame
from FirstProj.models import BaselineData
from FirstProj.models import Disease
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.db.models import Q
import numpy as np


def run():
    disease = 'HIV'
    country_name = 'Democratic Republic of the Congo'
    query = Disease.objects.all()
    qs2 = Disease.objects.get(disease_name=disease)
    data = BaselineData.objects.filter(Q(disease=qs2)).values()
    plt.style.use('Solarize_Light2')
    df = read_frame(data, fieldnames=['country_name', 'incidence_2020', 'incidence_2021', 'incidence_2022'])
    df.fillna(-1, inplace=True)

    def most_recent(row):
      if row['incidence_2022'] != -1:
        return row['incidence_2022']
      elif row['incidence_2021'] != -1:
        return row['incidence_2021']
      elif row['incidence_2020'] != -1:
        return row['incidence_2020']
      else:
        return None

    df['incidence'] = df.apply(most_recent, axis=1)
    df = df.loc[df['incidence'] > 0]
    df.sort_values(by='incidence', inplace=True)
    countries = df['country_name'].values.tolist()
    incidences = df['incidence'].values.tolist()
    country = df.loc[df['country_name'] == country_name]['incidence'].values[0]
    pos = incidences.index(country)
    logs = df['incidence']**.5
    low = min(logs)
    bars = plt.bar(countries, logs,)
    bars[pos].set_color('orange')
    bars[pos].set_label(country_name)
    bars[round(len(incidences)/2)].set_color('black')
    bars[round(len(incidences)/2)].set_label(f'Median Incidence ({countries[round(len(incidences)/2)]})')
    plt.legend()
    plt.xticks([])
    plt.xlabel('Countries', color='black', fontweight='bold', fontsize='14', horizontalalignment='center')
    plt.ylabel('$\sqrt{Incidence\quad (per\quad 100,000)}$', color='black', fontweight='bold', fontsize='14')
    plt.title('{} Incidence Rates by Country'.format(disease))
    plt.show()
    buf = BytesIO()
    #plt.savefig(buf, format='png')
    #buf.seek(0)
    #string = base64.b64encode(buf.read())
    return #string.decode('utf-8')
