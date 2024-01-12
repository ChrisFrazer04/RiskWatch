import json
import urllib.request
import urllib.parse
import requests
import sqlite3
import math

class gapi_request:
    def __init__(self):
        self.serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
        self.api_key = 'AIzaSyAkqT5NcD8JHNfdPqy2iVWqkLDv9Kl208A'

    def make_request_gmaps(self, address):
        params = {}
        params['key'] = self.api_key
        params['latlng'] = address
        self.enc_params = urllib.parse.urlencode(params)
        url = self.serviceurl + self.enc_params
        response = requests.get(url)
        self.rawjs = response.json()
        self.text = json.dumps(self.rawjs, indent=4)
        return self.text

    def get_stats(self):
        data = self.rawjs
        stats = {}
        data = data['results'][0]
        lat = data['geometry']['location']['lat']
        lng = data['geometry']['location']['lng']
        coordinates = list()
        coordinates.append(lat)
        coordinates.append(lng)
        stats['coordinates (lat/lng)'] = coordinates
        stats['types'] = data['types']
        #Change this part to reflect administrative levels and such
        stats['address'] = data['formatted_address']
        for thing in data['address_components']:
            for item in thing['types']:
                if item == 'locality':
                    stats['locality_data'] = thing
                if item == 'administrative_area_level_1':
                    stats['admin_1'] = thing
                if item == 'administrative_area_level_2':
                    stats['admin_2'] = thing
                if item == 'administrative_area_level_3':
                    stats['admin_3'] = thing
                if item == 'postal_code':
                    stats['zip_code'] = thing
                if item == 'country':
                    stats['country_data'] = thing
        return stats
    def get_coordinates(self):
        data = self.rawjs
        data = data['results'][0]
        lat = data['geometry']['location']['lat']
        lng = data['geometry']['location']['lng']
        return [float(lat), float(lng)]
    def get_coordinates_text(self):
        data = self.rawjs
        data = data['results'][0]
        lat = data['geometry']['location']['lat']
        lng = data['geometry']['location']['lng']
        return str(lat) + ',' + str(lng)
    def get_address(self):
        """Returns the country name and formatted address"""
        locale = self.get_stats()
        results = {}
        results['country'] = locale['country_data']['long_name']
        results['address'] = locale['address']
        return results
    def calc_distance(self, address, target):
        self.make_request_gmaps(address)
        var_name = self.another('var_name')
        var_name.make_request_gmaps(target)
        coords2 = var_name.get_coordinates()
        coords1 = self.get_coordinates()
        lat1 = coords1[0]
        lng1 = coords1[1]
        lat2 = coords2[0]
        lng2 = coords2[1]
        def haversine_formula(lat1, lng1, lat2, lng2):
            R = 6371000
            phi_1 = math.radians(lat1)
            phi_2 = math.radians(lat2)
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lng2 - lng1)
            a = math.sin(delta_phi/2)**2 + math.cos(phi_1)*math.cos(phi_2)*math.sin(delta_lambda/2)**2
            c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
            meters = R * c
            km = meters/1000
            km = round(km, 3)
            return km
        distance = haversine_formula(lat1, lng1, lat2, lng2)
        return distance
    def another(self, name):
        name = gapi_request()
        return name
    def search_nearby(self, location, radius_meters, type, keyword=None):
        #https://developers.google.com/maps/documentation/places/web-service/search-nearby#maps_http_places_nearbysearch-py
        self.make_request_gmaps(location)
        #location2 = self.get_coordinates_text()
        location_data = self.get_address()
        serviceurl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        params = {}
        params['location'] = location
        params['key'] = self.api_key
        params['radius'] = radius_meters
        params['type'] = type
        params['keyword'] = keyword
        url = serviceurl + urllib.parse.urlencode(params)
        response = requests.get(url)
        self.nearby_js = response.json()
        self.nearby_text = json.dumps(self.nearby_js, indent=4)
        count = 0
        for entry in self.nearby_js['results']:
            count +=1
        density = count*1000/radius_meters
        values = dict()
        values['density'] = density
        values['country'] = location_data['country']
        values['address'] = location_data['address']
        return values



