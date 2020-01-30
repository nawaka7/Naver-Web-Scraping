from mlxtend.preprocessing import OnehotTransactions
from mlxtend.frequent_patterns import apriori
import datetime
import pandas as pd
from Crawler_Naver_T02 import naver_keywords

# # KIN
# file_name = 'parsed_dict_20190304.txt'
# with open(file_name, mode='rt', encoding='utf-16') as file:
#     print('readable: ', file.readable())
#     data_dict = eval(file.read())
# # preprocessing
# data_dict_1 = dict()
# for company in data_dict.keys():
#     txt = data_dict[company]
#     txt = re.sub(r'\xa0','', txt)
#     txt = re.sub(r'\xad', '', txt)
#     txt = re.sub('[.|!|?]', '스플릿지점',txt)
#     txt = re.sub('[~!@#$%^&*()_+?><":}{.,;]*', '', txt)
#     data_dict_1[company] = re.split("스플릿지점", txt)
#
# t_now = datetime.datetime.now()
# with open('2khaiii_MBA_' + str(t_now.date()).replace('-', '') + '.txt', mode='wt', encoding='utf-16') as file:
#     file.write(str(data_dict_1))


# morpheme by Khaiii
file_name1 = 'parse_sen_dict.txt'
with open(file_name1, mode= 'rt', encoding= 'utf-16') as file:
    print('readable: ', file.readable())
    data_dict1 = eval(file.read())

# preprocessing
# preprocessing
filter_words = set()
add_lst = '답변 신청 카페 추가 나오'.split()
for word in add_lst:
    filter_words.add(word)
data_dict_proc = dict()
for company in data_dict1.keys():
    data_dict_proc[company] = list()
    for lst in data_dict1[company]:
        if len(lst) == 0:
            continue
        else:
            temp_lst = [morph_pair[0] for morph_pair in lst if morph_pair[0] not in filter_words]
            if len(temp_lst) > 0:
                data_dict_proc[company].append(temp_lst)

selected_words = set('MBPS 셋탑 빠르 기본료 스마트 채널 UHD 기가인터넷 초고속인터넷 무료 회선 업체 일반'.split())

data_dict_slct = dict()
for company in data_dict1.keys():
    data_dict_slct[company] = list()
    company_name = set([company])
    for basket in data_dict_proc[company]:
        check = False
        for item in basket:
            if item in company_name:
                check = True
                break
        if check is True:
            data_dict_slct[company].append(basket)
    print(len(data_dict_slct[company]))

data_dict_slct2 = dict()
for company in data_dict1.keys():
    data_dict_slct2[company] = list()
    for basket in data_dict_slct[company]:
        check = False
        for item in basket:
            if item in selected_words:
                check = True
                break
        if check is True:
            data_dict_slct2[company].append(basket)
    print(len(data_dict_slct2[company]))


if __name__ == '__main__':
    for company in data_dict_slct2.keys():
        oht = OnehotTransactions()
        oht_ary = oht.fit(data_dict_slct2[company]).transform(data_dict_slct2[company])
        df = pd.DataFrame(oht_ary, columns= oht.columns_)
        print(df.iloc[0,0])

    frequent_itemsets = apriori(df, min_support= 0.01, use_colnames= True)



frozenset({'인터넷', 'TV', '상품'})
frozenset({'사은품', '인터넷', '가입', '문의'})
frozenset({'인터넷', '요금', '휴대폰'})
frozenset({'약정', '고객'})
frozenset({'인터넷', '가입', '회선'})
frozenset({'인터넷', '통신사'})
frozenset({'인터넷', '결합', '약정'})
frozenset({'할인'})
frozenset({'결합', '통신사', '인터넷'})
frozenset({'결합', '할인', '약정', '가입'})