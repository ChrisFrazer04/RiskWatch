from FirstProj.models import BaselineData
from FirstProj.models import Disease
from FirstProj.models import Country

def funct(country, disease):
    dis = Disease.objects.get(disease_name=disease)
    data = BaselineData.objects.filter(disease=dis).values()
    data_ctr_specific = BaselineData.objects.filter(disease=dis, country_name=country).values()
    value_specific = data_ctr_specific[0]['incidence']
    value_list = list()
    for item in data:
        value = item['incidence']
        value_list.append(value)
    value_list.sort(reverse=True)
    final = value_list.index(value_specific)
    text = '{} has the 25th highest {} incidence rates '.format(country, disease)
    print(final)
    return final

def run():
    country='Kenya'
    disease='Malaria'
    funct(country, disease)