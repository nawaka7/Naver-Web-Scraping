from mlxtend.preprocessing import OnehotTransactions
from mlxtend.frequent_patterns import apriori
import datetime
import pandas as pd
from Crawler_Naver_T02 import naver_keywords

from apyori import apriori
from functools import reduce
from itertools import combinations, product, permutations
import seaborn as sn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
 
# file upload & pre-processing
file_dir = 'D:\\python3_JHC\\SKB_Rep_Crawling\\'
file_name = '0313kinnparsed_dict.txt'
with open(file_dir + file_name, mode= 'rt', encoding = 'utf-16') as file:
    data_dict = eval(file.read())
 
data_dict_proc = dict()
for key in data_dict.keys():
    data_dict_proc[key] = list()
    for doc in data_dict[key]:
        for sen in doc:
            if len(sen) > 0:
                data_dict_proc[key].append(set([word[0] for word in sen]))
 
 
 
# apriori by keywords
## freq count
# All docs together
total_docs = list(reduce(lambda x, y: x + y, list(data_dict_proc.values())))
print("total N: ", len(total_docs))
 
keywords = '속도 빠르 느리 안정 좋 나쁘 핑 낮 높'.split()
companies = list(data_dict.keys())
temp_key_lst = keywords + companies
# frequency count
freq_dict = dict()
for key in temp_key_lst:
    freq_dict[key] = 0
    for sentence in total_docs:
        if key in sentence:
            freq_dict[key] += 1
print(freq_dict)
 
result_dict = dict()
for onepair in freq_dict.keys():
    result_dict[onepair] = [freq_dict[onepair], freq_dict[onepair]/len(total_docs),1,1]
 
#self-join
twopairs = list()
threepairs = list()
for i in range(0,3):
    twopairs_temp = list(product(companies, [keywords[i*3]]))
    twopairs += twopairs_temp
    for pair in twopairs_temp:
        for j in [i*3+1,i*3+2]:
            threepair_temp = list(pair)
            threepair_temp.append(keywords[j])
            threepairs.append(tuple(threepair_temp))
 
combinations = twopairs + threepairs
comb_cnt_dict = dict()
for comb in combinations:
    comb_cnt_dict[comb] = 0
    for sentence in total_docs:
        if sum([1 for word in comb if word in sentence]) == len(comb):
            comb_cnt_dict[comb] += 1
 
 
for pair in twopairs:
    result_dict[pair] = [comb_cnt_dict[pair], comb_cnt_dict[pair]/len(total_docs),
                            comb_cnt_dict[pair]/result_dict[pair[0]][0],
                            (comb_cnt_dict[pair]/result_dict[pair[0]][0])/(result_dict[pair[1]][1])]
 
 
 
for pair in threepairs:
    try:
        result_dict[pair] = [comb_cnt_dict[pair], comb_cnt_dict[pair]/len(total_docs),
                                comb_cnt_dict[pair]/result_dict[pair[:2]][0],
                                (comb_cnt_dict[pair]/result_dict[pair[:2]][0])/(result_dict[pair[2]][1])]
    except:
        result_dict[pair] = [0, 0, 0, 0]
 
col_lst = [str(key) for key in list(result_dict.keys())]
df = pd.DataFrame(index= col_lst,
                 columns= 'frequency support confidence lift'.split())
 
 
for key in result_dict.keys():
    print(key)
    df.loc[str(key)] = result_dict[key]
 
 
# visualizing 예시
# data selection
data= df.iloc[9:11+1]
# graph
sn.set(style= "whitegrid", font= 'SeoulHangangC')
ax = sn.barplot(x=list(data.index), y= 'frequency', data= data, palette=['#FF0000','#2d72d9', '#598C14'])
ax.set_title("\"브랜드\" 빈도수", fontsize = 15, x=0.5, y=1.1)
n=0
for p in ax.patches:
    x = p.get_x()
    y = p.get_height()
    txt = "{}%".format('%.2f'%round(df.loc[data.index[n]]['support']*100,3))
    plt.text(x+0.25, y+100, s= txt, va = 'center', ha = 'left')
    n+=1
