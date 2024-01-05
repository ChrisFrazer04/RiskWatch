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
      except:
        country = hospital['country_name']
        risk = 'Locations in {} are currently not supported for {}.'.format(country, disease_real)
        text = 'Supported countries include: {}'.format(hospital['text'])
      try:
        factors = results['factors']
        args = {'form':form, 'text':text, 'risk':risk, 'factors': factors, 'graph': graph}
      except:
        args = {'form': form, 'text': text, 'risk': risk}

    return render(request, self.template_name, args)

  def calculate_risk(self, country, disease, location_data):
    dis = Disease.objects.get(disease_name=disease)
    data = BaselineData.objects.filter(disease=dis).values()
    data_ctr_specific = BaselineData.objects.filter(disease=dis, country_name=country).values()
    value_specific = data_ctr_specific[0]['incidence']
    value_list = list()
    for item in data:
      value = item['incidence']
      value_list.append(value)
    value_list.sort(reverse=True)
    length = len(value_list)
    final = value_list.index(value_specific) + 1
    results = dict()
    value_list2 = self.nonzero_list(value_list)
    length = len(value_list2)
    incidence = value_specific
    if incidence == 0:
      risk = 'Risk: None'
      text = 'There were no reported cases of {} in {}'.format(disease, country)
      results['text'] = text
      results['risk'] = risk
    else:
      median = self.get_median(value_list2)
      if location_data['large'] == 0:
        incidence = incidence*1.05
      if location_data['small'] > 0:
        incidence = incidence*1.05
      if incidence >= median*8:
        risk = 'Very High'
      elif incidence >= median*4:
        risk = 'High'
      elif incidence >= median*2:
        risk = 'Moderate'
      elif incidence >= median/2:
        risk = 'low'
      elif incidence >= median/4:
        risk = 'Very low'
      elif incidence < median/4:
        risk = 'Minimal'
      risk_text = 'Risk: {}'.format(risk)
      text = '{} has the {}th highest {} incidence rate out of {} countries with reported {} cases '.format(country, final, disease, length, disease)
      results['text'] = text
      results['risk'] = risk_text
      results['magnitude'] = incidence/median
      results['factors'] = 'Factors accounted for: Hospital Density'
      results['graph'] = self.get_graph(dis, disease)
    return results

  def hospital_density(self, location, disease):
    small_rad = 2000
    medium_rad = 4000
    large_rad = 6000
    maps = gapi_request()
    densities = dict()
    small = maps.search_nearby(location=location, radius_meters=small_rad, type='hospital')
    country = small['country']
    supported = self.check_supported(disease, country)
    if supported == True:
      medium = maps.search_nearby(location=location, radius_meters=medium_rad, type='hospital')
      large = maps.search_nearby(location=location, radius_meters=large_rad, type='hospital')
      densities['small'] = small['density']
      densities['medium'] = medium['density']
      densities['large'] = large['density']
      densities['country'] = small['country']
      return densities
    else:
      results = dict()
      results['text'] = supported
      results['country_name'] = country
      return results

  def get_median(self, nums):
    length = len(nums)
    if length / 2 == round(length / 2):
      median_index1 = round(length / 2)
      median_index2 = round(length / 2) + 1
      median = (nums[median_index1] + nums[median_index2]) / 2
    else:
      median_index = round(length / 2)
      median = nums[median_index]
    return median

  def nonzero_list(self, nums):
    nums.sort()
    for num in nums:
      if num > 0:
        nonzero_index = nums.index(num)
        break
    new_nums = nums[nonzero_index:]
    new_nums.sort(reverse=True)
    return new_nums

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

  def get_graph(self, queryset, disease):
    plt.style.use('ggplot')
    qs = BaselineData.objects.filter(Q(disease=queryset) & Q(incidence__gt=0)).values()
    df = read_frame(qs, fieldnames=['country_name', 'incidence'])
    ok = df.sort_values(by='incidence').plot.bar(x='country_name', y='incidence', label='Incidence (per 100,000)')
    ok.set_xticks([])
    plt.xlabel('Countries', color='black', fontweight='bold', fontsize='14', horizontalalignment='center')
    # plt.ylabel('Incidence (per 100,000)', color='black', fontweight='bold', fontsize='14')
    plt.title('{} Incidence Rates by Country'.format(disease))
    # plt.show()
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



