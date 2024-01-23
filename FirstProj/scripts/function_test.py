from FirstProj.AppCode.GMAPS_API import gapi_request
from FirstProj.models import BaselineData
from FirstProj.models import Disease
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django_pandas.io import read_frame
from django.db.models import Q
from FirstProj.models import Country
import pandas as pd
import numpy as np


def funct(disease, country):
    dis = Disease.objects.get(disease_name=disease)
    data = BaselineData.objects.filter(disease=dis).values()
    try:
        # Country is supported
        test = BaselineData.objects.get(disease=dis, country_name=country)
        return True
    except:
        # Country not supported
        value_dict = dict()
        value_list = list()
        value_text = ''
        for item in data:
            value = item['country_name']
            value_list.append(value)
            value_text += ' {},'.format(value)
        value_text = value_text[:-1]
        value_dict['text'] = value_text
        value_dict['list'] = value_list
        print(value_dict)
        return value_dict

def calculate_risk(country, disease, location_data):
    dis = Disease.objects.get(disease_name=disease)
    data = BaselineData.objects.filter(disease=dis).values()
    data_ctr_specific = BaselineData.objects.filter(disease=dis, country_name=country).values()
    df = read_frame(data, fieldnames=['country_name','incidence_2020','incidence_2021','incidence_2022'])
    df.fillna(-1, inplace=True)
    def most_recent(row):
        if row['incidence_2022'] != -1:
            return row['incidence_2022']
        elif row['incidence_2021'] != -1:
            return row['incidence_2021']
        elif row['incidence_2020'] != -1:
            return row['incidence_2020']
        else: return None
    df['incidence'] = df.apply(most_recent, axis=1)
    nonzero_incidences = df.loc[df['incidence'] > 0]['incidence'].values.tolist()
    incidence = df.loc[df['country_name'] == country]['incidence'].values[0]
    median = np.median(nonzero_incidences)
    results = {}
    if incidence == 0:
        risk = 'Risk: None'
        text = 'There were no reported cases of {} in {}'.format(disease, country)
        results['text'] = text
        results['risk'] = risk
    else:
        final = nonzero_incidences.index(incidence) + 1
        if location_data['small'] == 0:
            incidence = incidence * 1.05
            if location_data['medium'] == 0:
                incidence = incidence * 1.05
                if location_data['large'] == 0:
                    incidence = incidence * 1.05
        if incidence >= median * 8:
            risk = 'Very High'
        elif incidence >= median * 4:
            risk = 'High'
        elif incidence >= median * 2:
            risk = 'Moderate'
        elif incidence >= median / 2:
            risk = 'low'
        elif incidence >= median / 4:
            risk = 'Very low'
        elif incidence < median / 4:
            risk = 'Minimal'
        risk_text = 'Risk: {}'.format(risk)
        text = f'{country} has the {final}th highest {disease} incidence rate out of {len(nonzero_incidences)} countries with reported {disease} cases '
        results['text'] = text
        results['risk'] = risk_text
        results['magnitude'] = incidence / median
        results['factors'] = 'Factors accounted for: Hospital Density'
        results['graph'] = self.get_graph(dis, disease)
    print(results)
    return results

def run():
    country = 'Kenya'
    disease = 'Malaria'
    locationdata = {
        'large': 1,
        'small': 1,
        'medium': 1
    }
    calculate_risk(country, disease, locationdata)
