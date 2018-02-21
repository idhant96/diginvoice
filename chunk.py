import multiprocessing
from core.utils.new import Big
import pandas as pd
import time
import sys

df = pd.read_excel(
            'csvs/top500.xlsx'
        )
df = df.fillna('')
df['MatchSearchName'] = ''
df['match'] = ''
# num_processes = multiprocessing.cpu_count()
startTime = time.time() * 1000
chunk_size = int(df.shape[0]/3)

chunks = [df.ix[df.index[i:i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]

pool = multiprocessing.Pool(processes=3)

writer = pd.ExcelWriter('newcode.xlsx')
objects = []
for i in range(len(chunks)):
    for j in range(len(chunks)):
        if i <= j:
            objects.append((chunks[i], chunks[j]))
# print(len(chunks))
# print(objects[0][0].head(n=2))
# print(objects[0][1].head(n=2))
# input('firt')
# print(objects[1][0].head(n=2))
# print(objects[1][1].head(n=2))
# input()
# print(objects[2][0].head(n=2))
# print(objects[2][1].head(n=2))
# sys.exit()

result = pool.starmap(Big.dup, objects)

# row = 1
# newdf = pd.DataFrame(columns=list(result[0].columns.values))
# newdf.to_excel(writer, 'sheet1')

# for i in range(len(result)):
#     result[i].to_excel(writer, 'sheet1', startrow=row, startcol=0, header=False)
#     row = row + len(result[i].index) + 1
for p in result:
    for pos1 in p.keys():
        df.at[pos1, 'MatchSearchName'] = df.iloc[pos1, 2]
        df.at[pos1, 'match'] = p[pos1]

df.to_excel(writer, 'sheet1')
writer.save()
print('complete ', time.time() * 1000 - startTime)
