# from core.utils import Big
import pandas as pd
from demo import Big
import time

startTime = time.time() * 1000
bigdata = pd.read_excel(
            'dummy.xlsx'
        )
bigdata = bigdata.fillna('')
x = bigdata.to_records()
for ob in x:
    print(ob[3])

# # smalldata = bigdata[['name','email','mobile','gender','city', 'speciality']].copy()
# writer = pd.ExcelWriter('Mock_result.xlsx')
# bigdata = bigdata.fillna('')
# # smalldata = smalldata.fillna('')
# # bigdata['age'] = ''
# bigdata['MatchSearchName'] = ''
# bigdata['match'] = ''
# # print(bigdata.head())
# bigdata = Big.dup(bigdata=bigdata)
# bigdata.to_excel(writer, 'sheet1')
# writer.save()
# print('complete ', time.time() * 1000 - startTime)
