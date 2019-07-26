## KOLIBRI Cloud API daemon example with access token
##### Purpose:
This example code shows basic access to the KOLIBRI Cloud API using a access token from KELLER to gather measurement data from the KOLIBRI Cloud. 
The API's specification can be found here: https://api.kolibricloud.ch/swagger/index.html?url=/swagger/v1/swagger.json

Endpoints interest are:

| Endpoint      | Use to       |  
| ------------- | :----------- | 
| ```GET /v1/Devices```      | Gets information of all devices | 
| ```GET /v1/Devices/{deviceId}```     | Gets information of a specific device  | 
| ```GET /v1/Measurements``` | Gets a list of measurements composed of a value and a UTC datetime | 

##### Needs:
+ **Python 2.7**  (Untested with Python 3.x)
+ **urllib2**

 It is necessary to have a valid *ACCESS_TOKEN*
 Please ask KELLER AG (kolibri@keller-druck.com) to provide a valid *ACCESS_TOKEN* key

##### Notes:
DateTime format from the API are always in **UTC**  
Pressure values from the API are always in **bar**  
Temperature values from the API are always in **°C**  
It is not possible to delete measurement data with the API  

If you want to try out the API with [Swagger](https://api.kolibricloud.ch/swagger/index.html?url=/swagger/v1/swagger.json) please us the dark green [Authorize] button and a valid bearer token. You can get a valid bearer token when logged in on www.kolibricloud.ch under [User Settings]
The ```deviceId``` are the same numbers that can be seen in the URL of the WebApp when the device is selected: [https://www.kolibricloud.ch/devices/**1234**/](https://www.kolibricloud.ch/devices/1234/)

If you want a permament *ACCESS_TOKEN*, please contact the KOLIBRI support team (kolibri@keller-druck.com).
The provided access token must be the value with the key "userOid" in the header of every request.
<img src="https://i.imgur.com/BtOYz6h.png" width="400">

If you plan run this as a server script to store measurement data from the KOLIBRI Cloud API the following procedure is recommended:
+ Decide for a time span to gather date: eg. Every 24h
+ Create a list of the ```deviceId```s that needs to be monitored (eg. ```my_devices=[1234,1235,1236]```)
+ Create a list of MeasurementsDefinitonIds representing the physical measurement channel (eg. ```channels_of_interest=[2,5,7,8,11]```)
+ Run the program every ~24h and
  - for all devices of interest...
  - for all channels of interest..
  - use ```get_data_measurements_from_timespan()``` with he timespan of ~24
  - and store the data into a DB
  - you might check first if the measuremenent(value+timestamp) is not already stored
+ It is possible that a request fails. To solve this error case please re-call the data later again. You might gather data from an overlapped time slot and exclude measurements that has been stored already.

Please create github issues for feature wishes or problems 
Or contact kolibri@keller-druck.com
