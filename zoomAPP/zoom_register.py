import time
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import json
import pandas as pd

import os.path

class configure:
    data={}
    @classmethod
    def load_parameters(cls,fileName):
        with open(fileName,'r') as config:
            cls.data = json.loads(config.read())
    @classmethod
    def get_working_folder_name(cls):
        return cls.data['working_folder']
    @classmethod
    def get_registrants_file_name(cls):
        return cls.data['registrants_file']
    @classmethod
    def get_meeting_id(cls):
        return cls.data['meeting_id']
    @classmethod
    def get_account_id(cls):
        return cls.data['account_id']
    @classmethod
    def get_client_id(cls):
        return cls.data['client_id']
    @classmethod
    def get_client_secret(cls):
        return cls.data['client_secret']


###!!! be careful of the 'meetings' or 'webinars'
###!!! in r = requests.put(f'https://api.zoom.us/v2/meetings/{meeting_id}/registrants/status',verify=False, headers=headers, data=json.dumps(payload))

def getToken():
    auth_server_url = 'https://zoom.us/oauth/token'
    #tm.jol.p@gmail.com
    account_id = configure.get_account_id()
    client_id = configure.get_client_id()
    client_secret = configure.get_client_secret()

    #tergarmingjue@gmail.com
    #account_id = 'IQYLsrm2QJabmnywtA7DVg'
    #client_id = 'K7kRhBM_R8KohbPFBv1h7A'
    #client_secret = 'qpPTJ5EZ4tceq21PL88eazziK1WkoqNF'
    token_req_payload = {'grant_type': 'account_credentials','account_id':account_id}
    token_response = requests.post(auth_server_url, \
                    data=token_req_payload, verify=False, allow_redirects=False,\
                    auth=(client_id, client_secret))

    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server"+token_response.status_code)
    tokens = json.loads(token_response.text)

    return tokens['access_token']


def approve_registrant(email,registrant_id,meeting_id,headers):
    payload = {"action": "approve","registrants": [{"email": email,"id":registrant_id}]}
    r = requests.put(f'https://api.zoom.us/v2/meetings/{meeting_id}/registrants/status',verify=False, headers=headers, data=json.dumps(payload))
    status_code = r.status_code
    if status_code == 200:
        print("return 200")
    if status_code == 204:
        print("Registrant status updated")

def registrant_id_exists(idfile):
    if(not os.path.exists(idfile)):
        with open(idfile, 'w') as fp:
            pass
        
def add_registrant_test():
    email ="guiqian.zhou@gmail.com"
    first_name = "桂花"
    last_name = "周"

    payload = { 'email':email, 'first_name':first_name, 'last_name': last_name }
    r = requests.post(f'https://api.zoom.us/v2/meetings/{meeting_id}/registrants', verify=False, headers=headers, data=json.dumps(payload))

    status_code = r.status_code
    y = json.loads(r.text)
    registrant_id_exists(registrant_id_file)
    if status_code == 201:
            registrant_id = y["registrant_id"]
            topic = y["topic"]
            print(f"Email: {email}, registrant id: {registrant_id}")
            registrant_id_dataframe = pd.DataFrame.from_records({'registrant_id':[registrant_id],'Email':[email]})
            registrant_id_dataframe.to_csv(registrant_id_file,mode='a')
            approve_registrant(email,registrant_id)
    elif status_code == 400:
            error_message = y["message"]
            print("response -> {}, error message -> {}".format(r, error_message))
    else:
            print(f"status code -> {status_code}")

def add_meeting_registrant(configFile):
    configure.load_parameters(configFile)
    meeting_id = configure.get_meeting_id()  # 83847820499
    print('meeting id:'+meeting_id)
    registrant_id_file = configure.get_working_folder_name()+"registrant_id.csv"
    registrant_id_exists(registrant_id_file)
    #add_registrant_test()
    registrant_file_name = configure.get_working_folder_name()+configure.get_registrants_file_name()
    print("Got the registrant file:"+registrant_file_name)
    headers = {'authorization': 'Bearer %s' % getToken(), 'content-type': 'application/json'}
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    table_dict= pd.read_excel(registrant_file_name,engine='openpyxl')
    df = pd.DataFrame(table_dict)
    payload = {} 
    for i in range(len(df['Email'])):
        email = df['Email'][i]
        first_name = df['First Name'][i]
        last_name = df['Last Name'][i]
        if str(email)!="nan":
            payload = {'email':email,'first_name':first_name,'last_name':last_name}
            r = requests.post(f'https://api.zoom.us/v2/meetings/{meeting_id}/registrants', verify=False, headers=headers, data=json.dumps(payload))
            time.sleep(2)
            status_code = r.status_code
            y = json.loads(r.text)

            if status_code == 201:
                    registrant_id = y["registrant_id"]
                    topic = y["topic"]
                    print(f"Email: {email}, registrant id: {registrant_id}")
                    registrant_id_dataframe = pd.DataFrame({'registrant_id':[registrant_id],'Email':[email]})
                    registrant_id_dataframe.set_index('registrant_id', inplace=True)
                    registrant_id_dataframe.to_csv(registrant_id_file,mode='a',header=False)
                    approve_registrant(email,registrant_id,meeting_id,headers)
            elif status_code == 400:
                    error_message = y["message"]
                    print("response -> {}, error message -> {}".format(r, error_message))
            else:
                    print(f"status code -> {status_code}")

def delete_meeting_registrant(reg_id):
  r = requests.delete(f'https://api.zoom.us/v2/meetings/{meeting_id}/registrants/{reg_id}', verify=False, headers=headers)
  status_code = r.status_code
  print(status_code)

if __name__ == '__main__':            
    # total arguments
    n = len(sys.argv)
    if n==2:
        configFile = sys.argv[1]
    else:
        sys.exit("run zoom_register.py configFile")
    
    add_meeting_registrant(configFile)
    #approve_registrant(email,'S1-IRfb7ScGHFvX8UlLdkQ')  
    #delete_meeting_registrant('AIj0w5GYTg-rJ2GTQBqzGg')
