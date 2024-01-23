from FirstProj.AppCode.WHO_API_2 import api_request
from FirstProj.models import BaselineData
from FirstProj.models import Disease
from FirstProj.models import Baseline
from FirstProj.models import Country
import pandas as pd

def get_diseases():
    """Returns a list of all disease names in the Disease table """
    diseases = Disease.objects.all()
    data = diseases.values('disease_name')
    disease_list = list()
    for item in data:
        disease = item['disease_name']
        disease_list.append(disease)
    return disease_list

def get_country_data(country):
    """Takes a country code and returns the country name, population,
    and code"""
    data = {}
    ctr = Country.objects.filter(country_code=country).values()
    data['country_name'] = ctr[0]['country_name']
    data['2020'] = ctr[0]['pop2020']
    data['2021'] = ctr[0]['pop2021']
    data['2022'] = ctr[0]['pop2022']
    return data

def get_api_data(indicator, disease):
    """Takes an indicator code and disease, inputting the incidence
    per 100k population for 2020,2022,2023 in the BaselineData table"""
    BASEURL = 'https://ghoapi.azureedge.net/api/'
    indicator = indicator
    params = "?$filter= SpatialDimType eq 'COUNTRY' and NumericValue ne null"
    tst = api_request(BASEURL)
    tst.set_addon(indicator)
    tst.set_params(params)
    tst.get_url()
    output = tst.make_request()
    if indicator == 'HIV_0000000026':
        output = output.loc[:, ['SpatialDim', 'TimeDim', 'NumericValue', 'Dim1']]
        data = output.loc[(output['TimeDim'] == 2020) & (output['Dim1'] == 'SEX_BTSX')].rename(columns={'NumericValue': '2020'})[['SpatialDim', '2020']]
        data2 = output.loc[(output['TimeDim'] == 2020) & (output['Dim1'] == 'SEX_BTSX')].rename(columns={'NumericValue': '2021'})[['SpatialDim', '2021']]
        data3 = output.loc[(output['TimeDim'] == 2020) & (output['Dim1'] == 'SEX_BTSX')].rename(columns={'NumericValue': '2022'})[['SpatialDim', '2022']]
    else:
        output = output.loc[:, ['SpatialDim', 'TimeDim', 'NumericValue']]
        data = output.loc[output['TimeDim'] == 2020].rename(columns={'NumericValue': '2020'})[['SpatialDim', '2020']]
        data2 = output.loc[output['TimeDim'] == 2021].rename(columns={'NumericValue': '2021'})[['SpatialDim', '2021']]
        data3 = output.loc[output['TimeDim'] == 2022].rename(columns={'NumericValue': '2022'})[['SpatialDim', '2022']]
    data = data.merge(data2, on='SpatialDim', how='outer').merge(data3, on='SpatialDim', how='outer')
    data.rename(columns={'SpatialDim': 'country_code'}, inplace=True)
    data.fillna(-1, inplace=True)
    #data['country_name'] = range(len(data.iloc[:, 0]))
    def insert_row(row):
        data = get_country_data(row['country_code'])
        MOD = 100000
        # [2020,2021,2022,code,name]
        entry = [row['2020']*MOD/data['2020'], row['2021']*MOD/data['2021'],
                     row['2022']*MOD/data['2022'], row['country_code'], data['country_name']]
        for item in entry[:3]:
            if item < 0:
                entry[entry.index(item)] = None
        new_entry = disease.baselinedata_set.create(incidence_2020=entry[0], incidence_2021=entry[1],
                                                        incidence_2022=entry[2], country_code=entry[3], country_name=entry[4])
        new_entry.save()
        print('Done')
        return
    data.apply(insert_row, axis=1)
    return 'Done'

def run():
    """Deletes all objects in the BaselineData table, then calls the get_api_data
     function for each disease, inputting data including country name, country
     code, and incidence per 100k for each country"""
    a = BaselineData.objects.all()
    a.delete()
    diseases = get_diseases()
    print(diseases)
    for disease in diseases:
        dis = Disease.objects.get(disease_name=disease)
        data = Baseline.objects.filter(disease=dis).values()
        indicator = data[0]['indicator_code']
        get_api_data(indicator=indicator, disease=dis)



