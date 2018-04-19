# This Python file uses the following encoding: utf-8
# ##############################################################################
# KOLIBRI CLOUD API DAEMON EXAMPLE WITH ACCESS TOKEN                         #
#                                                                            #
# Needs:                                                                     #
# - Python 2.7  (Untested with Python 3.x)                                   #
# - Installed adal (Microsoft Azure Active Directory Authentication Library) #
# - urllib2                                                                  #
#                                                                            #
# It is necessary to have a valid parameters CLIENT_SECRET + ACCESS_TOKEN    #
# Please ask KELLER to provide a valid parameters                            #  
#                                                                            #  
# DateTime format from the API are always in UTC                             #
# Pressure values from the API are always in bar                             #
# Temperature values from the API are always in °C                           #
##############################################################################
import json
import logging
import os
import sys
import adal  # See Installation Usage @ https://github.com/AzureAD/azure-activedirectory-library-for-python
import urllib2
from datetime import timedelta
import datetime

# parameters:
TENANT = "kellerdruckcloud.onmicrosoft.com"
GRAPH_RESOURCE = '415b2501-0867-4c06-82cf-2a37115484be'
RESOURCE = "https://"+TENANT+"/"+GRAPH_RESOURCE
AUTHORITY_HOST_URL = "https://login.microsoftonline.com"
AUTHORITY_URL = AUTHORITY_HOST_URL + '/' + TENANT
CLIENT_ID = "a4df092f-dbc1-460b-894c-9b8d9a8a8fa1"
# parameters client specific
CLIENT_SECRET = "modified_K/FVCGP0f5NpIG8p15cKp7ejv0L9aSYE="
ACCESS_TOKEN = "modified_Wn74ULdF7yWye+4MMkCE8h7WTpwx0c/nxA91j4IwMHpOispTmxE2jh76IH/6SuKtRlaLFNsaP/JClz99nuebbVo5Tc0RokWq/37xClKuPfmTamLq/m5j2ThLPeuGj9mhICECGM2M9RqWtdHLM/s/AAAAABzqRTG/XOVILk8fq7stsfOlHoHudIDGbianypbFE+zfHxE4CKI1IZAaTEWkHEGQcA==" # represents the user


def turn_on_logging_of_imported_libraries():
    """ Use this to get more log information from the ADAL library and the urllib2
        For debug purpose.
    """
    logging.basicConfig(level=logging.DEBUG)

def get_bearer_token(authority_url, resource, client_id, client_secret):   
    """
    Gets the Bearer Token that is needed authentication.
    Do not use this more than once a hour.
    """
    context = adal.AuthenticationContext(authority_url, validate_authority=['tenant']!='adfs', api_version=None)
    token_json_obj = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
    return token_json_obj['accessToken']

def get_data(_endpoint, _bearer_token, _access_token):
    """
    With the correct Bearer Token and the correct Access Token one can get data from the API.
    The API specification can be seen here: 
    https://api.kolibricloud.ch/swagger/index.html?url=/swagger/v1/swagger.json
    """
    base_url = "https://api.kolibricloud.ch"
    url = base_url + _endpoint
    req = urllib2.Request(url)
    req.add_header("Authorization","Bearer %s" %_bearer_token)
    req.add_header("userOid",_access_token)
    try:
        response = urllib2.urlopen(req) 
    except urllib2.HTTPError, e: print e.headers
    html = response.read()
    json_obj = json.loads(html)
    return json_obj

def get_measurementDefinitionId_LookUpTable():
    measurementDefinitionId_LookUpTable = {
        1 : "Pd (P1-P2) in [bar]",
        2 : "P1 in [bar]",
        3 : "P2 in [bar]",
        4 : "T in °C",
        5 : "TOB1 in °C",
        6 : "TOB2 in °C",
        7 : "PBaro in [bar]",
        8 : "TBaro in [°C]",
        9 : "Volt Inp. 1 in [V]",
        10: "Volt Inp. 2 in [V]",
        11: "Pd (P1-PBaro) in [bar]",
        12: "Conductivity Tc in [mS/cm]",
        13: "Conductivity raw in [mS/cm]",
        14: "T (Conductivity) in [°C]",
        15: "P1 (2) in [bar]",
        16: "P1 (3) in [bar]",
        17: "P1 (4) in [bar]",
        18: "P1 (5) in [bar]",
        19: "Counter input",
        20: "SDI12 CH1",
        21: "SDI12 CH2",
        22: "SDI12 CH3",
        23: "SDI12 CH4",
        24: "SDI12 CH5",
        25: "SDI12 CH6",
        26: "SDI12 CH7",
        27: "SDI12 CH8",
        28: "SDI12 CH9",
        29: "SDI12 CH10"
        }
    return measurementDefinitionId_LookUpTable

def get_data_measurements_from_timespan(timespan_in_hours, measurementDefinitionId, deviceId, _bearer_token, _access_token):
    get_measurement_data_timespan = timedelta(hours=timespan_in_hours)
    end_time   = datetime.datetime.utcnow()
    start_time = end_time - get_measurement_data_timespan
    endpoint = "/v1/Measurements?measurementDefinitionId="+str(measurementDefinitionId)+"&deviceId="+str(deviceId)+"&start="+str(start_time.isoformat()+'Z')+"&end="+str(end_time.isoformat()+'Z')
    data = get_data(endpoint, _bearer_token, _access_token)
    return data

#uncomment for verbose log
#turn_on_logging_of_imported_libraries()

print("Getting bearer token...")
bearer_token = get_bearer_token(AUTHORITY_URL, RESOURCE, CLIENT_ID, CLIENT_SECRET)
print(".... bearer token found"+"\n")

# with the bearer token and the access on can access the data from the API
# here are some examples
endpoint = "/v1/Devices"
print("Here are the list of all devices:")
data1 = get_data(endpoint, bearer_token, ACCESS_TOKEN)
print(json.dumps(data1, indent=2))
print("----------------------------------------------------"+"\n")

my_device = data1["devices"][0]["id"]
#my_device = 1234  # must be a device id that is in the set of accessible devices
endpoint = "/v1/Devices/"+str(my_device)
data2 = get_data(endpoint, bearer_token, ACCESS_TOKEN)
print("Here are information of device "+str(my_device)+":")
print("(If you do not own #"+str(my_device)+" this will break here.)")
print(json.dumps(data2, indent=2))
print("----------------------------------------------------"+"\n")
#print('Last measurement time was: '+data2['lastMeasurementTransmissionDateTime'])


# data3 is the JSON data from device "my_device" of the channel with the id 2 which is P1 in [bar] of the last 12 hours
measurementDefinitionId = 2 #  is P1 / See get_measurementDefinitionId_LookUpTable()
data3 = get_data_measurements_from_timespan(12, measurementDefinitionId, my_device, bearer_token, ACCESS_TOKEN)
measurementDefinitionIds = get_measurementDefinitionId_LookUpTable()
print("Measurements of " + measurementDefinitionIds[measurementDefinitionId]+" : ")
print(json.dumps(data3, indent=2))
print("----------------------------------------------------"+"\n")


print("The list of the device ids and their channels: ")
for each_device in data1['devices']:
    endpoint = "/v1/Devices/"+str(each_device['id'])
    data = get_data(endpoint, bearer_token, ACCESS_TOKEN)
    all_channels_of_this_device = []
    for each_channel in data['measurementDefinitions']:
        all_channels_of_this_device.append(str(each_channel['id'])+":"+each_channel['name'])
    all_channels_of_this_device = [str(all_channels_of_this_device[x]) for x in range(len(all_channels_of_this_device))] #just stringify more beautiful
    print("#"+str(each_device['id'])+" has measurement channels: "+str(all_channels_of_this_device))