import json
import sqlite3
import time
import requests
import csv
import pandas as pd

class api_request:
    def __init__(self, serviceRoot):
        self.serviceRoot = serviceRoot
        self.addon = ''
        return

    def set_addon(self, addon):
        self.addon = addon
        return addon

    def set_params(self, params):
        self.params = params
        return params

    def get_url(self):
        url = self.serviceRoot + self.addon + self.params
        return url

    def make_request(self):
        """Makes a get request to WHO Api, returning response json,
        response text, and status message"""
        url = self.get_url()
        output = {}
        response = requests.get(url)
        output['json'] = response.json()
        output['text'] = json.dumps(response.json(), indent=4)
        output['status'] = response.status_code
        ind_df = pd.json_normalize(output['json']['value'])
        return ind_df



#contains_example = 'https://ghoapi.azureedge.net/api/Indicator' + "?$filter=contains(IndicatorName, 'HIV')"
