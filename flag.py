import pandas as pd


class Flag(object):
    # tamilnadu = pd.read_csv('csvs/tamilnadu.csv')
    # tamil_docs = pd.read_csv('csvs/TamilNaiduDoctors.csv')
    docs = pd.read_csv('csvs/docs.csv')
    # print(tamil_docs['District'])
    town_names = {}
    population = {}
    district_names = []
    docs.corr
    # for pos, obj in tamilnadu.iterrows():
    #     town = obj['Town Name']
    #     town = town[0:town.index('(')].strip()
    #     if town not in town_names:
    #         town_names[town.upper()] = pos
    #     if obj['District Name'] not in district_names:
    #         district_names.append(obj['District Name'].upper())
    # print(town_names)
    # for district in district_names:
    #     for town in town_names.keys():
    #         if district == town:
    #             print(town, tamilnadu['Total Population of Town'].iloc[town_names[town]])
    #             # population[town] =
