from FirstProj.AppCode.WHO_API import api_request
from FirstProj.models import BaselineData
from FirstProj.models import Disease
from FirstProj.models import Baseline
from FirstProj.models import Country

def get_diseases():
    diseases = Disease.objects.all()
    data = diseases.values('disease_name')
    disease_list = list()
    for item in data:
        disease = item['disease_name']
        disease_list.append(disease)
    return disease_list

def get_api_data(indicator, disease):
    baseurl = 'https://ghoapi.azureedge.net/api/'
    indicator = indicator
    year = 2021
    params = "?$filter= TimeDim eq {} and SpatialDimType eq 'COUNTRY' and NumericValue ne null".format(year)
    tst = api_request()
    tst.set_serviceRoot(baseurl)
    tst.set_addon(indicator)
    tst.set_params(params)
    tst.get_url()
    tst.make_request()
    data = tst.rawjs
    values = dict()
    value_list = list()
    for ctr in data['value']:
        country = ctr['SpatialDim']
        country_data = get_country_data(country)
        country_name = country_data['country_name']
        country_code = country_data['country_code']
        population = country_data['population']
        raw_value = ctr['NumericValue']
        modifier = 100000/float(population)
        incidence_per_100k = float(raw_value) * modifier
        value_list.append(incidence_per_100k)
        new_entry = disease.baselinedata_set.create(country_code=country_code, country_name=country_name, incidence=incidence_per_100k)
        new_entry.save()

    return 'Done'

def get_country_data(country):
    data = dict()
    ctr =  Country.objects.filter(country_code=country).values()
    data['country_name'] = ctr[0]['country_name']
    data['country_code'] = ctr[0]['country_code']
    data['population'] = ctr[0]['population']
    return data

def run():
    a = BaselineData.objects.all()
    a.delete()
    diseases = get_diseases()
    print(diseases)
    for disease in diseases:
        dis = Disease.objects.get(disease_name=disease)
        data = Baseline.objects.filter(disease=dis).values()
        indicator = data[0]['indicator_code']
        get_api_data(indicator=indicator, disease=dis)



