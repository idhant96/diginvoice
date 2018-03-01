from core.utils.new import Big
import pandas as pd
import time
import sys


path = sys.argv[1]
odf = pd.read_excel(path)
startTime = time.time() * 1000
result = Big.process_dataframe(path)
# df['MatchSearchName'] = ''
# df['match'] = ''
# print(result)
# cols = ['pos','name', 'email', 'mobile', 'gender', 'age', 'city', 'speciality']

df = pd.DataFrame(columns=list(odf.columns.values))
# df = pd.DataFrame()
writer = pd.ExcelWriter('500res.xlsx')
added = []
for gender in result:
    for p in gender:
        for pos1 in p.keys():
            for pos2 in p[pos1]:
                flag = 0
                for tup in added:
                    if pos1 in tup and pos2 in tup:
                        flag = flag + 1
                if flag > 0:
                    continue
                df = df.append(odf.loc[odf['Doctor Code'] == pos1])
                df = df.append(odf.loc[odf['Doctor Code'] == pos2])
                added.append((pos1, pos2))


            # df.at[pos1, 'MatchSearchName'] = df.iloc[pos1, 2]
            # df.at[pos1, 'match'] = p[pos1]
print(added)
df.to_excel(writer, 'sheet1')
writer.save()
print('complete ', time.time() * 1000 - startTime)
