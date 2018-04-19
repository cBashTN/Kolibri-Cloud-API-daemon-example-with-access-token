## KOLIBRI Cloud API daemon example with access token
##### Purpose:
This example code shows basic access to the KOLIBRI Cloud API which is specification can be seen here: https://api.kolibricloud.ch/swagger/index.html?url=/swagger/v1/swagger.json

##### Needs:
+ **Python 2.7**  (Untested with Python 3.x)
+ **Installed adal** (Microsoft Azure Active Directory Authentication Library) 
    (https://github.com/AzureAD/azure-activedirectory-library-for-python)
+ **urllib2**

 It is necessary to have a valid parameters *CLIENT_SECRET* + *ACCESS_TOKEN*
 Please ask KELLER AG to provide a valid parameters

##### Notes:
 DateTime format from the API are always in UTC
 Pressure values from the API are always in bar
 Temperature values from the API are always in °C

If you plan run this as a server script to store measurement data from the KOLIBRI Cloud API the following procedure is recommended:
+ Decide for a time span to gather date: eg. Every 24h
+ Create a list of the DeviceIds that needs to be monitored (eg. ```my_devices=[1234,1235,1236]```)
+ Create a list of MeasurementsDefinitonIds representing the physical measurement channel (eg. ```channels_of_interest=[2,5,7,8,11]```)
+ Run the program every ~24h and
  - for all devices of interest...
  - for all channels of interest..
  - use ```get_data_measurements_from_timespan()``` with he timespan of ~24
  - and store the data into a DB
  - you might check first if the measuremenent(value+timestamp) is not already stored