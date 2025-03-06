import pandas as pd
import numpy as np

registrant_id_file = "../JOL1_202309/registrant_id2.csv"
#registrant_id_dataframe = pd.DataFrame.from_records({'registrant_id':'m6WfU8UTRze7EF-maV9tLw','Email':'guiqian.zhou@gmail.com'}, index=['registrant_id'])
registrant_id_dataframe = pd.DataFrame(np.array([['guiqian.zhou@gmail.com','m6WfU8UTRze7EF-maV9tLw']]),columns = ['Email','registrant_id'])  #,columns = ['Email','registrant_id']
registrant_id_dataframe.to_csv(registrant_id_file,mode='a')
