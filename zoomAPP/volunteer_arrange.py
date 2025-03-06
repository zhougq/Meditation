import pandas as pd

file_name = "../VolunteerWorkApril2022/Volunteer_03_15_2022_GH.xlsx"

output_file = "../VolunteerWorkApril2022/Candidates.xlsx"

volunteer_work= ['注册','清洁','会场布置','搬运东西',\
                 '音响','网络','Gift','插花',\
                 '住所','话筒','取餐',\
                 '接送','陪同','茶水',\
                 '座位','杂事']
work_count = len(volunteer_work)
Candidates =['']* work_count

table_dict= pd.read_excel(file_name,engine='openpyxl')
df = pd.DataFrame(table_dict)
for i in range(len(df['WorkYouLike'])):
   for j in range(work_count):
      if volunteer_work[j] in df['WorkYouLike'][i]:
         Candidates[j]+=df['Name'][i]+';'

out_df = pd.DataFrame(zip(volunteer_work,Candidates))
out_df.to_excel(output_file,engine='openpyxl')


