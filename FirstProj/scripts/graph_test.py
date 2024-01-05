from django_pandas.io import read_frame
from FirstProj.models import BaselineData
from FirstProj.models import Disease
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.db.models import Q


def run():
    disease = 'Rubella'
    query = Disease.objects.all()
    qs2 = Disease.objects.get(disease_name=disease)
    qs3 = BaselineData.objects.filter(Q(disease=qs2) & Q(incidence__gt=0)).values()
    plt.style.use('ggplot')
    df = read_frame(qs3, fieldnames=['country_name', 'incidence'])
    ok = df.sort_values(by='incidence').plot.bar(x='country_name', y='incidence', label='Incidence (per 100,000)')
    ok.set_xticks([])
    plt.xlabel('Countries', color='black', fontweight='bold', fontsize='14', horizontalalignment='center')
    #plt.ylabel('Incidence (per 100,000)', color='black', fontweight='bold', fontsize='14')
    plt.title('{} Incidence Rates by Country'.format(disease))
    plt.show()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string.decode('utf-8')
