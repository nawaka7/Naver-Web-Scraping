import requests as rq
from itertools import product


# Naver companies & keywords
naver_id = "ZGSTXXq2qZ9jk2ZrdVwQ"
naver_secret = "bMAWepRXfv"
naver_companies = "SK, LG, KT".split(', ')
naver_keywords_web = "인터넷 가입, 인터넷 설치, 인터넷 현금, 인터넷 사은품, 인터넷 할인, 인터넷 변경, 인터넷 통신사, 티비 인터넷 결합, 인터넷 가격 비교, " \
                 "설치 가능 지역, 인터넷 안정성, 인터넷 속도, 인터넷 약정, 인터넷 해지, 인터넷 상담, 인터넷 요금 비교, 인터넷 위약금".split(", ")
naver_keywords_tv= []
search_keywords = '해지, 약정, 가입, 사은품, 결합, 할인, 비교, 요금, VOD, 채널, 다시보기, 키즈'.split(', ')
tv_keywords = 'TV 티비 IPTV'.split()
for comb in product(tv_keywords, search_keywords):
    naver_keywords_tv.append(comb[0] + ' ' + comb[1])
# page type
page_types = 'kin news webkr cafearticle blog'.split()


def res_req_naver_Web(naver_id, naver_secret, keywords_lst1, keywords_lst2, page_types, format= '.json', display= 100):
    '''
    :param naver_id: naver_id for log-in type Naver open API requests (string)
    :param naver_secret: naver_secret for log-in type Naver open API requests (string)
    :param keywords_lst1: 1st keywords that will be used as the keys in the dictionary to be returned (list)
    :param keywords_lst2: 1st keywords that will be used as the keys in the dictionary to be returned (list)
    :param page_types: page types available in Naver open API (list)
    :param format: .json or .xml (string)
    :param display: 10~100 (integer)
    :return: dictionary (json)
    '''
    nn_result_dict = {}
    for keyword1 in keywords_lst1:
        nn_result_dict.update({keyword1: {}})
        for keyword2 in keywords_lst2:
            nn_result_dict[keyword1].update({keyword2: {}})
            # request get
            encText = rq.utils.requote_uri(keyword1 + " " + keyword2)
            for page_type in page_types:
                # URL
                url = "https://openapi.naver.com/v1/search/" + page_type + format + "?query=" + encText + "&display=" + str(display) # json 결과, + 검색페이지수는 display<=100
                nn_response_code = rq.get(url, headers={"X-Naver-Client-Id": naver_id, "X-Naver-Client-Secret": naver_secret})

                try:
                    if nn_response_code.status_code == 200:
                        plain = nn_response_code.text
                        plain_dict = eval(plain)
                        nn_result_dict[keyword1][keyword2].update({page_type: plain_dict['items']})
                        print(keyword1, keyword2)
                    else:
                        print("Status Code Not 200")
                except Exception as e:
                    print("ERROR: Code: {c}, Message, {m}".format(c = type(e).__name__, m = str(e)))

    return nn_result_dict


def res_req_naver_TV(naver_id, naver_secret, keywords_lst1, keywords_lst2, page_types, format= '.json', display= 100):
    '''
    :param naver_id: naver_id for log-in type Naver open API requests (string)
    :param naver_secret: naver_secret for log-in type Naver open API requests (string)
    :param keywords_lst1: 1st keywords that will be used as the keys in the dictionary to be returned (list)
    :param keywords_lst2: 1st keywords that will be used as the keys in the dictionary to be returned (list)
    :param page_types: page types available in Naver open API (list)
    :param format: .json or .xml (string)
    :param display: 10~100 (integer)
    :return: dictionary (json)
    '''
    nn_result_dict = {}
    for keyword1 in keywords_lst1:
        nn_result_dict.update({keyword1: {}})
        for keyword2 in keywords_lst2:
            if keyword1 == 'LG':
                nn_result_dict[keyword1].update({keyword2: {}})
                add_lst = '유플러스 U+ U플러스'.split()
                for page_type in page_types:
                    nn_result_dict[keyword1][keyword2][page_type] = []
                    # URL
                    for add_keyword1 in add_lst:
                        # request get
                        encText = rq.utils.requote_uri(keyword1 + " " + add_keyword1 + " " + keyword2)
                        url = "https://openapi.naver.com/v1/search/" + page_type + format + "?query=" + encText + "&display=" + str(
                            int(display/3))  # json 결과, + 검색페이지수는 display<=100
                        nn_response_code = rq.get(url, headers={"X-Naver-Client-Id": naver_id,
                                                                "X-Naver-Client-Secret": naver_secret})

                        try:
                            if nn_response_code.status_code == 200:
                                plain = nn_response_code.text
                                plain_dict = eval(plain)
                                nn_result_dict[keyword1][keyword2][page_type] =+ plain_dict['items']
                                print(keyword1, keyword2)
                            else:
                                print("Status Code Not 200")
                        except Exception as e:
                            print("ERROR: Code: {c}, Message, {m}".format(c=type(e).__name__, m=str(e)))
            else:
                nn_result_dict[keyword1].update({keyword2: {}})
                # request get
                encText = rq.utils.requote_uri(keyword1 + " " + keyword2)
                for page_type in page_types:
                    # URL
                    url = "https://openapi.naver.com/v1/search/" + page_type + format + "?query=" + encText + "&display=" + str(display) # json 결과, + 검색페이지수는 display<=100
                    nn_response_code = rq.get(url, headers={"X-Naver-Client-Id": naver_id, "X-Naver-Client-Secret": naver_secret})

                    try:
                        if nn_response_code.status_code == 200:
                            plain = nn_response_code.text
                            plain_dict = eval(plain)
                            nn_result_dict[keyword1][keyword2].update({page_type: plain_dict['items']})
                            print(keyword1, keyword2)
                        else:
                            print("Status Code Not 200")
                    except Exception as e:
                        print("ERROR: Code: {c}, Message, {m}".format(c = type(e).__name__, m = str(e)))

    return nn_result_dict

def get_res():
    while True:
        key_res = input("choose a number in the following \n 1. internet \n 2. media \n ? >: ")
        if key_res in '1 2'.split():
            break
        else:
            print("\n ***** WARNING: CHOOSE 1 or 2 ***** \n")
    return key_res

# Naver Open API
key_res = get_res()

if key_res == '1':
    print("* your choice: only internet.")
    nv_result_dict = res_req_naver_Web(naver_id, naver_secret, naver_companies, naver_keywords_web, page_types)
elif key_res == '2':
    print("your choice: only TV.")
    nv_result_dict = res_req_naver_TV(naver_id, naver_secret, naver_companies, naver_keywords_tv, page_types)

if nv_result_dict is True:
    print("--- 100% ---- Naver Open API response all received")
else:
    print("Naver Open API response reception failed")