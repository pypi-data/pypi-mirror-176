# CloudConnect [![cloudconnect2](https://github.com/Oviing/CloudConnect/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Oviing/CloudConnect/actions/workflows/python-publish.yml)

This python package allows you easily retrieve destination information from the SAP BTP

### Usage

```python
from cloudconnect2 import load_destination
destinationName = "ABC API Name"
destinationService = "Service"
debugMode = False
destination = load_destination(destinationName, destinationService, debugMode)
````
- The destination name determines the name of the API destination in the SAP BTP you want to retrieve
- The destination service instead is the name of the service binding in the cloud foundry runtime the application wants to access
- the debug mode determines if we want to recieve just the toke or for development purpose only also other information

### Installation
To install the package execute the following command
```
python3 -m pip install git+https://github.com/Oviing/CloudConnect.git
```
If you are using jupyter notebook you have to use instead the following command
```
!python3 -m pip install git+https://github.com/Oviing/CloudConnect.git
```
Or easy via pip
```
pip install cloudconnect2
```
