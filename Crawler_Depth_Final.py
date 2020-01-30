import bs4
import requests as rq
from functools import reduce
from Crawler_Naver_Final import naver_keywords_tv, naver_keywords_web, naver_companies, key_res, nv_result_dict



def kin_crawl(data_dict, keywords_lst1, keywords_lst2):
    page_type = 'kin'
    d1_result_dict = dict()
    for keyword1 in keywords_lst1:
        d1_result_dict.update({keyword1: {}})

        for keyword2 in keywords_lst2:
            d1_result_dict[keyword1].update({keyword2: {}})
            n = 0 # start
            for doc in data_dict[keyword1][keyword2][page_type]:
                d1_result_dict[keyword1][keyword2].update({str(n): {}})
                URL2chk =  doc['link']
                code = rq.get(URL2chk)
                plain = code.text
                soup = bs4.BeautifulSoup(plain, "html5lib")

                doc_Id = URL2chk.split('docId=')[1].split('&qb=')[0]
                try:
                    d_data_area = soup.find_all('div', {'class': 'c-userinfo__left'})
                    d_data_span = str(d_data_area[0].find_all('span', {"class": "c-userinfo__date"})[0]).split('작성일')[1]
                    d_data = str(reduce(lambda x, y: x + y, re.findall('\d',d_data_span)))
                except:
                    print('no date data: no document presumed to exist')
                    d_data = ''
                t_data = soup.find_all('div', {'class': 'title'})
                q_data = soup.find_all('div', {'class': 'c-heading__content'})
                a_data = soup.find_all('div', {'class': '_endContentsText c-heading-answer__content-user'})

                d1_result_dict[keyword1][keyword2][str(n)]['doc_Id'] = doc_Id

                try:
                    d1_result_dict[keyword1][keyword2][str(n)]['date'] = d_data
                except IndexError:
                    d1_result_dict[keyword1][keyword2][str(n)]['date'] = ''
                try:
                    d1_result_dict[keyword1][keyword2][str(n)]['title'] = str(list(t_data)[0])
                except IndexError:
                    d1_result_dict[keyword1][keyword2][str(n)]['title'] = ''
                try:
                    d1_result_dict[keyword1][keyword2][str(n)]['question'] = str(list(q_data)[0])
                except IndexError:
                    d1_result_dict[keyword1][keyword2][str(n)]['question'] = ''
                try:
                    a_data_lst = []
                    for elm in list(a_data):
                        a_data_lst.append(str(elm))
                    d1_result_dict[keyword1][keyword2][str(n)]['answer'] = a_data_lst
                except IndexError:
                    d1_result_dict[keyword1][keyword2][str(n)]['answer'] = []

                print(keyword1, keyword2, n)

                n += 1

    return d1_result_dict


if key_res == '1':
    d1_kin_dict = kin_crawl(nv_result_dict, naver_companies, naver_keywords_web)
else:
    d1_kin_dict = kin_crawl(nv_result_dict, naver_companies, naver_keywords_tv)