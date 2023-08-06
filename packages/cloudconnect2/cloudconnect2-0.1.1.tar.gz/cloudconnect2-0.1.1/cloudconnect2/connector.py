from cfenv import AppEnv

import base64
import requests



def load_destination(destinationName, destinationService, token_url, debugMode = False):
    env = AppEnv()
    destination_service = env.get_service(name = destinationService)

    destination_credentials = destination_service.credentials
    id = destination_credentials["clientid"]
    secret= destination_credentials["clientsecret"]
    url = destination_credentials["url"]
    JWT_TOKEN_URL = url + "/oauth/token"

    byte_string = id + ":" + secret
    string_to_bytes = bytes(byte_string, "utf-8")
    base64_bytes = base64.b64encode(string_to_bytes)
    base64_string = base64_bytes.decode()
    headers = {'Authorization': 'Basic '+base64_string, 'content-type': 'application/x-www-form-urlencoded'}
    form = [('client_id', id ), ('grant_type', 'client_credentials')]
    r = requests.post(JWT_TOKEN_URL, data=form, headers=headers)
    token = r.json()["access_token"]

    #Get token for Default service keys
    headers= { 'Authorization': 'Bearer ' + token }
    r = requests.get(token_url + '/destination-configuration/v1/destinations/'+destinationName, headers=headers)
    token = r.json()

    if debugMode == True:
        debugJSON = {"id": id,
                    "secret": secret,
                    "url" : url,
                    "token" : token
        }
        return debugJSON
    else:

        return token