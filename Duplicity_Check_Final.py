from itertools import combinations
from functools import reduce
from copy import deepcopy
from Crawler_Naver_Final import naver_keywords_tv, naver_keywords_web, naver_companies, key_res
from Crawler_Depth_Final import d1_kin_dict


if key_res == '1':
    naver_keywords = naver_keywords_web
else:
    naver_keywords = naver_keywords_tv

# check the duplicity
id_dict = dict()
for company in naver_companies:
    id_dict[company] = []
    for keyword in naver_keywords:
        id_dict[company].extend(([d1_kin_dict[company][keyword][str(n)].get('doc_Id') for n in list(range(len(d1_kin_dict[company][keyword])))]))
id_eda = dict() # total docs counts
for company in id_dict.keys():
    id_eda[company] = {}
    id_eda[company]['total'] = len(id_dict[company])
    print(company, 'total docs: ', len(id_dict[company]))

ids_cnt = dict() # by company, count all the ids
for company in id_dict.keys():
    ids_cnt[company] = {}
    ids_lst = id_dict[company]
    ids_set = set(id_dict[company])
    for id in ids_set:
        ids_cnt[company][id] = ids_lst.count(id)

ids_cnt2 = dict() # within company, count duplicates
for company in id_dict.keys():
    ids_cnt2[company] = {k: v for k, v in ids_cnt[company].items() if v > 1}
for company in id_dict.keys():
    id_eda[company]['cnt_within'], id_eda[company]['perc_within']= len(ids_cnt2[company]), len(ids_cnt2[company])/len(set(id_dict[company]))
    print(company, 'overlap-within: ', id_eda[company]['cnt_within'], 'docs, ', round(id_eda[company]['perc_within'],3)*100, '%')

# between companies, count duplicates
# 2 pair
ids_cnt3 = dict()
for pair in combinations(tuple(naver_companies),2):
    ids_cnt3[pair] = [id for id in set(ids_cnt[pair[0]].keys()) if id in set(ids_cnt[pair[1]].keys())]

# 3 pair
for pair in combinations(tuple(naver_companies),3):
    ids_cnt3[pair] = [id for id in set(ids_cnt[pair[0]].keys()) if id in set(ids_cnt[pair[1]].keys()) and id in set(ids_cnt[pair[2]].keys())]
for pair in ids_cnt3.keys():
    id_eda[pair] = {}
    id_eda[pair]['cnt_btwn'], id_eda[pair]['perc_btwn'] = len(ids_cnt3[pair]), len(ids_cnt3[pair])/sum([id_eda[i]['total'] for i in pair])
    print(pair, 'overlap-between: ', id_eda[pair]['cnt_btwn'], 'docs ', round(id_eda[pair]['perc_btwn'],3)*100, '%')

#unique
ids_unique = dict()
for company in ids_cnt.keys():
    ids_unique[company] = [k for k, v in ids_cnt[company].items() if k not in set(reduce(lambda x, y: x + y, list(ids_cnt3.values())))]
for company in ids_unique.keys():
    id_eda[company]['cnt_unique'] = len(ids_unique[company])
    print(company, 'unique: ', id_eda[company]['cnt_unique'], 'docs ')




# project the data
ids_unique_2 = dict()
for company in ids_cnt.keys():
    ids_unique_2[company] = [k for k in set(ids_cnt[company].keys()) if k not in set(reduce(lambda x, y: x + y, list(ids_cnt3.values())))]
n= 0
result_dict = deepcopy(d1_kin_dict)
ids_set_2 = set(reduce(lambda x, y: x + y, list(ids_unique_2.values())))
for company in naver_companies:
    for keyword in naver_keywords:
        for num in d1_kin_dict[company][keyword]:
            doc_id = d1_kin_dict[company][keyword][num]['doc_Id']
            if doc_id in ids_set_2:
                n += 1
                ids_set_2.remove(doc_id)
            else:
                try:
                    del result_dict[company][keyword][num]
                except KeyError:
                    continue





# project the data: total docs with no over-representation
result_lst_total = list()
ids_set = set()
for lst in id_dict.values():
    temp_set = set(lst)
    ids_set = ids_set.union(temp_set)

n_1 = 0
for company in naver_companies:
    for keyword in naver_keywords:
        for num in d1_kin_dict[company][keyword]:
            if d1_kin_dict[company][keyword][num]['doc_Id'] in ids_set:
                result_lst_total.append(d1_kin_dict[company][keyword][num])
                n_1 += 1
                ids_set.remove(d1_kin_dict[company][keyword][num]['doc_Id'])
            else:
                pass