from core.utils import Big
import pandas as pd


bigdata = pd.read_excel(
            'MOCK_DATA.xlsx'
        )
writer = pd.ExcelWriter('Mock_result.xlsx')
bigdata = bigdata.fillna('')
bigdata['MatchSearchName'] = ''
bigdata['match'] = ''
bigdata, writer = Big.lol(bigdata=bigdata, writer=writer)
bigdata.to_excel(writer, 'sheet1')
writer.save()
