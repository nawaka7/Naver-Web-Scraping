from Crawler_Naver_Final import key_res
from Duplicity_Check_Final import result_dict, result_lst_total
from datetime import datetime



if __name__ == "__main__":
    if key_res == '1':
        choice = 'Web'
    else:
        choice = 'TV'

    t_now = datetime.now()
    with open(choice + '_kin_unique_dict_0402_' + str(t_now.date()).replace('-', '') + '.txt', mode='wt',
              encoding='utf-16') as file:
        file.write(str(result_dict))

    with open(choice + '_kin_unique_dict_total__' + str(t_now.date()).replace('-', '') + '.txt', mode='wt',
              encoding='utf-16') as file:
        file.write(str(result_lst_total))
