from GMAPS_API import gapi_request
from WHO_API import api_request

gmap = gapi_request()
gmap.search_nearby(location='University of Southern California', radius_meters=500, type='hospital')




exit()
baseurl = 'https://ghoapi.azureedge.net/api/'
indicator = 'NTD_YAWSNUM'
country='KEN'
params = "?$filter= SpatialDimType eq 'COUNTRY' and NumericValue ne null"
tst = api_request()
tst.set_serviceRoot(baseurl)
tst.set_addon(indicator)
tst.set_params(params)
tst.get_url()
tst.make_request()
data = tst.rawjs
text = tst.text
values = dict()
value_list = list()
for ctr in data['value']:
    country = ctr['SpatialDim']
    value = ctr['NumericValue']
    value_list.append(value)
    values[country] = value
#min = min(value_list)
#max = max(value_list)
print(text)

#print(values)
