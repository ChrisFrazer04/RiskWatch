from FirstProj.models import Disease
from FirstProj.models import Baseline

def create(disease, code, name):
    if disease.lower == 'done' or code.lower == 'done' or name.lower == 'done':
        return
    d = Disease(disease_name=disease)
    d.save()
    b = Baseline(disease=d, indicator_code=code, indicator_name=name)
    b.save()

def run():
    disease = 'none'
    while disease.lower != 'done':
        disease = input('Input disease here: ')
        code = input('Input Indicator Code: ')
        name = input('Input Indicator Name: ')
        create(disease, code, name)



