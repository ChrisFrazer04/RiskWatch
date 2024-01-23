from django.shortcuts import render, HttpResponse
from .forms import DistanceInput
from .forms import RiskCalculator
from django.views.generic import TemplateView
from FirstProj.AppCode.GMAPS_API import gapi_request
from FirstProj.models import BaselineData
from FirstProj.models import Disease
from FirstProj.forms import Testing
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django_pandas.io import read_frame
from django.db.models import Q
from FirstProj.models import Country
import json
import urllib.request
import urllib.parse
import requests
import sqlite3
import math
import numpy as np
# Create your views here.

def index(request, id):
  return HttpResponse("<h1> %s </h1>" % id)
  #return render(request, 'FirstProj/index.html')

def home(request):
  return render(request, 'FirstProj/index.html')

class Risk_Calculator(TemplateView):
  template_name = 'FirstProj/BackgroundSite.html'
  def get(self, request):
    form = RiskCalculator()
    return render(request, self.template_name, {'form':form})

  def post(self, request):
    form = RiskCalculator(request.POST)
    if form.is_valid():
      location = form.cleaned_data['location']
      diseases = form.cleaned_data['dropdown']
      disease_real = str(diseases)
      hospital = self.hospital_density(location, disease_real)
      try:
        country = hospital['country']
        results = self.calculate_risk(country=country, disease=disease_real, location_data=hospital)
        text = results['text']
        risk = results['risk']
        graph = results['graph']
        address = hospital['address']
      except:
        country = hospital['country']
        risk = 'Locations in {} are currently not supported for {}.'.format(country, disease_real)
        text = 'Supported countries include: {}'.format(hospital['text'])
      try:
        factors = results['factors']
        args = {'form':form, 'text':text, 'risk':risk, 'factors': factors, 'graph': graph, 'show': 'show'}
      except:
        args = {'form': form, 'text': text, 'risk': risk}

    return render(request, self.template_name, args)

  def calculate_risk(self, country, disease, location_data):
    """Takes a country name, disease name, and hospital density (location data),
    returning either an error message or the calculated disease risk"""
    dis = Disease.objects.get(disease_name=disease)
    data = BaselineData.objects.filter(disease=dis).values()
    data_ctr_specific = BaselineData.objects.filter(disease=dis, country_name=country).values()
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
      results['graph'] = self.get_graph(dis, disease, location_data['country'])
    return results

  def hospital_density(self, location, disease):
    """
    Takes a location and a disease, finding the density of hospitals around it.
    """
    small_rad = 2000
    medium_rad = 4000
    large_rad = 6000
    maps = gapi_request()
    densities = {}
    small = maps.search_nearby(location=location, radius_meters=small_rad, type='hospital')
    country = small['country']
    supported = self.check_supported(disease, country)
    #If the disease/country combo is inside of the database
    if supported == True:
      medium = maps.search_nearby(location=location, radius_meters=medium_rad, type='hospital')
      large = maps.search_nearby(location=location, radius_meters=large_rad, type='hospital')
      densities['small'] = small['density']
      densities['medium'] = medium['density']
      densities['large'] = large['density']
      densities['country'] = small['country']
      densities['address'] = small['address']
      return densities
    #Runs if the disease/country combo is not in the database
    else:
      results = {}
      results['text'] = supported
      results['country'] = country
      return results

  def check_supported(self, disease, country):
    dis = Disease.objects.get(disease_name=disease)
    data = BaselineData.objects.filter(disease=dis).values()
    try:
      #Country is supported
      test = BaselineData.objects.get(disease=dis, country_name=country)
      return True
    except:
      #Country not supported
      value_text = ''
      for item in data:
        value = item['country_name']
        value_text += ' {},'.format(value)
      value_text = value_text[:-1]
      return value_text

  def get_graph(self, queryset, disease, country_name):
    """Creates a graph """
    plt.style.use('Solarize_Light2')
    data = BaselineData.objects.filter(Q(disease=queryset)).values()
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
    country_val = df.loc[df['country_name'] == country_name]['incidence'].values[0]
    pos = incidences.index(country_val)
    sqrts = df['incidence'] ** .5
    bars = plt.bar(countries, sqrts)
    bars[pos].set_color('orange')
    bars[pos].set_label(country_name)
    bars[round(len(incidences) / 2)].set_color('black')
    bars[round(len(incidences) / 2)].set_label(f'Median Incidence ({countries[round(len(incidences) / 2)]})')
    plt.legend()
    plt.xticks([])
    plt.xlabel('Countries', color='black', fontweight='bold', fontsize='14', horizontalalignment='center')
    plt.ylabel('$\sqrt{Incidence\quad (per\quad 100,000)}$', color='black', fontweight='bold', fontsize='14')
    plt.title('{} Incidence Rates by Country'.format(disease))
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string.decode('utf-8')


class Distance_calc(TemplateView):
  template_name = 'FirstProj/distance_page.html'
  def get(self, request):
    form = DistanceInput()
    return render(request, self.template_name, {'form':form})

  def post(self, request):
    form = DistanceInput(request.POST)
    if form.is_valid():
      text1 = form.cleaned_data['location1']
      text2 = form.cleaned_data['location2']
      distance = self.distance(text1, text2)
      text = str(distance) + " kilometers"
    args = {'form':form, 'text':text}
    return render(request, self.template_name, args)

  def distance(self, location1, location2):
    var = gapi_request()
    distance = var.calc_distance(location1, location2)
    return distance

class Test(TemplateView):
  template_name = 'FirstProj/Testing.html'
  def get(self, request):
    form = Testing()
    return render(request, self.template_name, {'form':form})



