import requests
import json

meeting_id = '85662801228'
auth_server_url = 'https://zoom.us/oauth/token'
#tm.jol.p@gmail.com
#account_id = 'VMTISWB8Qtau7XVb2S720Q'
#client_id = '0dVxL2LsTFexU1UIbveRGA'
#client_secret = 'WSWyXZ7zXoEXIecj8fXbHe8clMkupxIx'

#tergarmingjue@gmail.com
account_id = 'IQYLsrm2QJabmnywtA7DVg'
client_id = 'K7kRhBM_R8KohbPFBv1h7A'
client_secret = 'qpPTJ5EZ4tceq21PL88eazziK1WkoqNF'

email ="mikezhymo@gmail.com"
first_name = "Mike"
last_name = "Mo"

def getToken():
    token_req_payload = {'grant_type': 'account_credentials','account_id':account_id}
    token_response = requests.post(auth_server_url, \
                    data=token_req_payload, verify=False, allow_redirects=False,\
                    auth=(client_id, client_secret))
#   Example from Zoom 
#    r = requests.post('https://zoom.us/oauth/token', -d 'grant_type=account_credentials'\
#                      -d 'account_id=5yiPLwmTTpQVBnMxOlf32q' -H 'Host: zoom.us'\
#                      -H 'Authorization: \
#                      Basic aGwbwxOgK6eGHEO0W1DOCv5WCODeVxoet7DFEON7bR23gP5qEW7cmeWCbCEO3ApBEWlRwCVpDWB=='

    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server"+token_response.status_code)
    tokens = json.loads(token_response.text)
#    print("token:" + tokens['access_token'])
    return tokens['access_token']

headers = {'authorization': 'Bearer %s' % getToken(), 'content-type': 'application/json'}

def add_meeting_registrant():    
    payload = { 'email':email, 'first_name':first_name, 'last_name': last_name }
    r = requests.post(f'https://api.zoom.us/v2/webinars/{meeting_id}/registrants', verify=False, headers=headers, data=json.dumps(payload))

    status_code = r.status_code
    y = json.loads(r.text)

    if status_code == 201:
            registrant_id = y["registrant_id"]
            topic = y["topic"]
            print(f"registrant id -> {registrant_id}, topic -> {topic}")
    elif status_code == 400:
            error_message = y["message"]
            print("response -> {}, error message -> {}".format(r, error_message))
    else:
            print(f"status code -> {status_code}")

def approve_registrant():
    payload = {"action": "approve","registrants": [{"email": email,"id":"px-1wv2zTU-HfnLzP4lebg"}]}
#    PUT /webinars/{webinarId}/registrants/status
    r = requests.put(f'https://api.zoom.us/v2/webinars/{meeting_id}/registrants/status',verify=False, headers=headers, data=json.dumps(payload))
    status_code = r.status_code
#    y = json.loads(r.text)
    if status_code == 200:
        print("return 200")
    if status_code == 204:
        print("Registrant status updated")

#add_meeting_registrant()
approve_registrant()

