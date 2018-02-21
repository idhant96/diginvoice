from core.utils.old import Big
import pandas as pd

import time


startTime = time.time() * 1000
bigdata = pd.read_excel(
            'csvs/top.xlsx'
        )
bigdata = bigdata.fillna('')
# print('1 ', time.time() * 1000 - startTime)

writer = pd.ExcelWriter('oldcode.xlsx')
bigdata = bigdata.fillna('')

bigdata['MatchSearchName'] = ''
bigdata['match'] = ''

bigdata = Big.dup(bigdata=bigdata)
bigdata.to_excel(writer, 'sheet1')
writer.save()
print('complete ', time.time() * 1000 - startTime)
