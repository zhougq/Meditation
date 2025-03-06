
import pandas as pd
import numpy as np
from datetime import date
import json

class configure:
    data ={}
    @classmethod
    def load_parameters(cls):
        with open('configure_202410.json','r') as config:
            cls.data = json.loads(config.read())
    @classmethod
    def get_working_folder_name(cls):
        return cls.data['working_folder']
    @classmethod
    def get_participants_report_file_name(cls):
        return cls.data['participants_report_file']
    @classmethod
    def get_registrants_file_name(cls):
        return cls.data['registrants_file']
    @classmethod
    def get_check_column(cls):
        return cls.data['check_column']
configure.load_parameters()

def do_statistics():
    participants_list = configure.get_working_folder_name()+configure.get_participants_report_file_name() #participants list
    registrants_file= configure.get_working_folder_name()+configure.get_registrants_file_name()   #registrants list
    check_column = ord(configure.get_check_column())-ord("A")
    today = date.today().strftime("%m-%d")

    table_dict_registrants= pd.read_excel(registrants_file,engine='openpyxl')
    df_registrants = pd.DataFrame(table_dict_registrants)
    len_registrants =len(df_registrants['Email'])

    table_dict_participants= pd.read_csv(participants_list)
    df_participants = pd.DataFrame(table_dict_participants)
    len_participants = len(df_participants['Email'])
 
    df = [0] * len_registrants

    #print(df_registrants.iloc[0][16])
    for i in range(len_registrants):
        if df_registrants.iloc[i][check_column] == '第一次':
            showup = False
            for j in range(len_participants):
                if df_participants['Email'][j].lower() == df_registrants['Email'][i].lower():
                    df[i] = int(df_participants['Total duration (minutes)'][j])
                    showup = True
                    continue
                #    print(df_registrants['Email'][i]+':'+str(df[i]))
            if (showup and df[i]<150):
            #        df.loc[row_index,col_indexer] 
                df_registrants.loc[i,today]='leave early('+str(df[i])+')'
            else:
                if (not showup):
                    df_registrants.loc[i,today]='no show'

    # In all participants, not in registrants list
    for j in range(len_participants):
        if df_registrants.iloc[i][check_column] == '第一次':
            found = 0
            for i in range(len_registrants):
                if (df_participants['Email'][j].lower() == df_registrants['Email'][i].lower()) :
                    found =1
                    continue
            if found == 0:
                print("Participants not in registrants list:"+df_participants['Email'][j])
            
    pd.DataFrame(df_registrants).to_excel(registrants_file,engine='openpyxl')
        
do_statistics()
