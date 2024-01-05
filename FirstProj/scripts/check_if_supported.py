from FirstProj.models import BaselineData
from FirstProj.models import Disease


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

def run():
    disease = 'Syphilis'
    country='Jamaica'
    funct(disease, country)
