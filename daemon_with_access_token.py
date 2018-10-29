# This Python file uses the following encoding: utf-8
# ##############################################################################
# KOLIBRI CLOUD API DAEMON EXAMPLE WITH ACCESS TOKEN                         #
#                                                                            #
# Needs:                                                                     #
# - Python 2.7  (Untested with Python 3.x)                                   #
# - urllib2                                                                  #
#                                                                            #
# It is necessary to have a valid  ACCESS_TOKEN.                             #
# Please ask KELLER to provide a valid ACCESS_TOKEN!                         #  
#                                                                            #  
# DateTime format from the API are always in UTC                             #
# Pressure values from the API are always in bar                             #
# Temperature values from the API are always in °C                           #
##############################################################################
import json
import logging
import os
import sys
import urllib2
from datetime import timedelta
import datetime

# client specific access token
ACCESS_TOKEN = "___modified___sVKKoibnUftMMkZlB9dFHFfWDoCDgu4wYSDvX3jXs16n+LJkpHcjDbdnObLVByQxn67yG/dczWMYrIjNd/s3qHyAAAAAMNB4dy+qNxTrW6TUVa/qk6/5esIKLuZbKG5D5eM34kpANDLOJzhcpBaOnZoNSvQgA==" # represents the user

def turn_on_logging_of_imported_libraries():
    """ Use this to get more log information from the ADAL library and the urllib2
        For debug purpose.
    """
    logging.basicConfig(level=logging.DEBUG)

def get_data(_endpoint, _access_token):
    """
    With the correct Access Token one can get data from the API.
    The API specification can be seen here: 
    https://api.kolibricloud.ch/swagger/index.html?url=/swagger/v1/swagger.json
    """
    base_url = "https://api.kolibricloud.ch"
    url = base_url + _endpoint
    req = urllib2.Request(url)
    req.add_header("userOid",_access_token)
    try:
        response = urllib2.urlopen(req) 
    except urllib2.HTTPError, e: print e.headers
    try:
        html = response.read()
        json_obj = json.loads(html)
    except UnboundLocalError:
        print("Could not find data in "+_endpoint+"\n")
        json_obj = ""
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
        29: "SDI12 CH10",
        30: "TOB1 (2)",
        31: "TOB1 (3)",
        32: "TOB1 (4)",
        33: "TOB1 (5)",
        34: "E",
        35: "F",
        36: "G",
        37: "mH20 (PBaro)",
        38: "mH20 (P1-P2)",
        39: "mH20 (P1-P3)",
        40: "mH20 (P1-P4)",
        41: "mH20 (P1-P5)",
        42: "Conductivity Tc (2)",
        43: "Conductivity Tc (3)",
        44: "T (Conductivity) (2)",
        45: "T (Conductivity) (3)",
        46: "P2 (2)",
        47: "TOB2 (2)"
    }
    return measurementDefinitionId_LookUpTable

def get_data_measurements_from_timespan(timespan_in_hours, measurementDefinitionId, deviceId, _access_token):
    get_measurement_data_timespan = timedelta(hours=timespan_in_hours)
    end_time   = datetime.datetime.utcnow()
    start_time = end_time - get_measurement_data_timespan
    endpoint = "/v1/Measurements?measurementDefinitionId="+str(measurementDefinitionId)+"&deviceId="+str(deviceId)+"&start="+str(start_time.isoformat()+'Z')+"&end="+str(end_time.isoformat()+'Z')
    data = get_data(endpoint, _access_token)
    return data

#uncomment for verbose log
#turn_on_logging_of_imported_libraries()

# with the access token you can access the data from the API without a bearer token
# here are some examples
endpoint = "/v1/Devices"
print("Here are the list of all devices:")
data1 = get_data(endpoint, ACCESS_TOKEN)
print(json.dumps(data1, indent=2))
print("----------------------------------------------------"+"\n")

my_device = data1["devices"][0]["id"] # or better use the specific device id my_device = 1234  # must be a device id that is in the set of accessible devices
endpoint = "/v1/Devices/"+str(my_device)
data2 = get_data(endpoint, ACCESS_TOKEN)
print("Here are information of device "+str(my_device)+":")
print("(If you do not own #"+str(my_device)+" this will break here.)")
print(json.dumps(data2, indent=2))
print("----------------------------------------------------"+"\n")
print('Last measurement time was: '+data2['lastMeasurementTransmissionDateTime'])


# data3 is the JSON data from device "my_device" of the channel with the id 8 which is TBaro in [° C] of the last 12 hours
measurementDefinitionId = 8 #  is TBaro (Air Temperature) / See get_measurementDefinitionId_LookUpTable()
data3 = get_data_measurements_from_timespan(12, measurementDefinitionId, my_device, ACCESS_TOKEN)
measurementDefinitionIds = get_measurementDefinitionId_LookUpTable()
print("Measurements of " + measurementDefinitionIds[measurementDefinitionId]+" : ")
print(json.dumps(data3, indent=2))
print("----------------------------------------------------"+"\n")


print("The list of the device ids and their channels: ")
for each_device in data1['devices']:
    endpoint = "/v1/Devices/"+str(each_device['id'])
    data = get_data(endpoint, ACCESS_TOKEN)
    all_channels_of_this_device = []
    for each_channel in data['measurementDefinitions']:
        all_channels_of_this_device.append(str(each_channel['id'])+":"+each_channel['name'])
    all_channels_of_this_device = [str(all_channels_of_this_device[x]) for x in range(len(all_channels_of_this_device))] #just prettify the texts
    print("#"+str(each_device['id'])+" has measurement channels: "+str(all_channels_of_this_device))