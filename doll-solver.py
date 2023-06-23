# packages uses in sorting chinese by pinyin
from itertools import chain
from pypinyin import pinyin, Style

# crawler packages
from fake_useragent import UserAgent
import requests
import re
import uuid
import time

##############################
# doll name sorting part start

# lowercase letters list
# used to sort chinese list by pinyin
lower_list = [chr(i) for i in range(ord('a'), ord('z') + 1)]


# a function call in sorting chinese by pinyin
def to_pinyin(s):
    if s in lower_list:
        return s
    return ''.join(chain.from_iterable(pinyin(s, style=Style.TONE3)))


# doll name sorting part end
##############################

##############################
# crawler part start

# randomly generate a proxy request
headers = {"User-agent": UserAgent().random,
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
           "Connection": "keep-alive"}

img_re = re.compile('"thumbURL":"(.*?)"')
img_format = re.compile("f=(.*).*?w")

# filename while saving image
filename = ''


# save the image
def file_op(img):
    uuid_str = uuid.uuid4().hex
    # tmp_file_name = 'arsenal/%s.jpeg' % uuid_str
    tmp_file_name = 'paipaile-level/' + filename + '.jpeg'
    with open(file=tmp_file_name, mode="wb") as file:
        try:
            file.write(img)
        except:
            pass


# crawling function
def xhr_url(url_xhr, start_num=0, page=5):
    end_num = page * 30
    for page_num in range(start_num, end_num, 30):
        resp = requests.get(url=url_xhr + str(page_num), headers=headers)
        if resp.status_code == 200:
            img_url_list = img_re.findall(resp.text)  # 这是个列表形式
            count = 0
            for img_url in img_url_list:
                count += 1
                # 爬取第三张图片
                if count == 3:
                    img_rsp = requests.get(url=img_url, headers=headers)
                    file_op(img=img_rsp.content)
                    # 爬取完成直接退出循环
                    break
            # 爬取完成直接退出循环
            break
        else:
            break
    # print("success")


# crawler part end
##############################


if __name__ == '__main__':

    ##############################
    # doll name sorting part start

    # doll name file
    doll_txt = open('paipaile-level.txt')
    # doll name list
    doll_list = doll_txt.read().splitlines()
    doll_list = list(set(doll_list))
    doll_txt.close()
    # add lowercase letters
    doll_list = doll_list + lower_list
    # sort doll name list by pinyin
    doll_list.sort(key=to_pinyin)
    # 'z'+1 is '{'
    doll_list.append(chr(ord('z') + 1))
    # dict: initial to doll names
    # doll_list[idx('z')+1:idx('z'+1)] return a slice correspond to the initial letter
    initial_dict = {lower: doll_list[doll_list.index(lower) + 1:doll_list.index(chr(ord(lower) + 1))]
                    for lower in lower_list}

    # save doll names to file
    # which is sorted by pinyin
    doll_sorted_txt = open('paipaile-level-sorted.txt', 'w')
    for s in doll_list:
        doll_sorted_txt.write(s)
        doll_sorted_txt.write('\n')
    doll_sorted_txt.close()

    # doll name sorting part end
    ##############################

    ##############################
    # doll picture crawling part start

    # crawling function calling example
    # org_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&word={text}&pn=".format(text=input("输入你想检索内容:"))
    # org_url = "https://image.baidu.com/search/index?ct=201326592&z=1&tn=baiduimage&ipn=r&word={text}".format(text=input("输入你想检索内容:")) + "&pn=&spn=&istype=2&ie=utf-8&oe=utf-8&cl=2&lm=-1&st=-1&fr=&fmq=&ic=0&se=&sme=&width=0&height=0&face=0&cs=&os=&objurl=&di=&gsm=5a "
    # xhr_url(url_xhr=org_url, start_num=int(input("开始页:")), page=int(input("所需爬取页数:")))
    # xhr_url(url_xhr=org_url, start_num=1, page=1)

    # crawl picture for each initial and each doll name
    for initial_key, doll_list_value in initial_dict.items():
        for doll_value in doll_list_value:
            filename = chr(ord(initial_key) - ord('a') + ord('A')) + doll_value
            org_url = "https://image.baidu.com/search/index?ct=201326592&z=1&tn=baiduimage&ipn=r&word={text}".format(text=doll_value)\
                      + "&pn=&spn=&istype=2&ie=utf-8&oe=utf-8&cl=2&lm=-1&st=-1&fr=&fmq=&ic=0&se=&sme=&width=0&height=0&face=0&cs=&os=&objurl=&di=&gsm=5a"
            xhr_url(url_xhr=org_url, start_num=1, page=1)
            print(filename)
            time.sleep(0.4)

    # doll picture crawling part end
    ##############################
