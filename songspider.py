# -*- coding:utf-8 -*-

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium import webdriver
import pandas as pd
import time
import os



def get_songs_link(url):
    global count
    global songsheet_num

    # selenium 请求url
    driver.get(url)
    print(f'--歌单[{songsheet_num}]:{url}')

    # 切换到frame标签
    driver.switch_to.frame('g_iframe')

    # 歌单信息
    link_list = []
    songsheets = driver.find_elements_by_xpath('//tbody/tr/td[2]/div/div/div/span/a')
    for song in songsheets:
        link = song.get_attribute('href')
        link_list.append(link)

    for link in link_list:
        print(f'[{songsheet_num}][{count}] ', link, 'start.')
        get_song_comments(link)
        count += 1

    songsheet_num += 1


def get_song_comments(url):

    # selenium 请求url
    driver.get(url)
    time.sleep(0.5)

    # 切换到frame标签
    driver.switch_to.frame('g_iframe')

    # 歌单信息
    name = driver.find_element_by_xpath('//div[@class="tit"]/em').text
    singer = driver.find_element_by_xpath('//p[@class="des s-fc4"]/span').get_attribute('title')
    comments_num = int(driver.find_element_by_xpath('//div[@class="n-cmt"]/div/div/span/span').text)

    # data = json.loads(str(requests.post(f'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{url.split("id=")[1]}?csrf_token=',
    #                                     headers={'User-Agent': UserAgent().random}, params=params, proxies={'http':'114.230.129.157:4257'}).content,
    #                       encoding="utf-8"))
    # comments_top = data['hotComments'][0]['content']
    # comments_top_num = data['hotComments'][0]['likedCount']

    songs_list.append([name, singer, url, comments_num])
    print(name, singer, url, comments_num)


if __name__ == '__main__':

    params = {
        'params': '0zAfAyEw6eOCWC27z2kKHul7hE/mk4lQMrLFFI5Eg+ngSnAW4JO+89rsob/F3p59vrxRTccCCRPP06QOUJWpCBbHK40eGGw/9z6qNpsjrqXcIPe7V9sl/tSlKze7Iq1jKNX8GiFKtIuCs7u0j6090ybyW9JEHde1aBYesJ22fFIP/nsvPE1d2nBTbOpqyG8I',
        'encSecKey': '9fc9414403f07adc50722e4bdc8ab0aee9cd41d7dafbb2c1ef3446bbc2fcca2bc77a50d7faed56abdf78e103c4dd73e2023950e62a7a78cc076d9f4ebcd480cb2982cef81f346c0a6ad4e7803a695e025a36608bed7b936ab994aa5f0f0895a6ff17e1864b427989da0418629a342dc53bf86e3699f38807747d901b2d932a9e'}

    # 无页面浏览器配置
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(UserAgent().random)
    chrome_options.add_argument(f'--proxy-server=http://111.75.155.74:4235')

    # 修改selenium页面加载策略
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"
    left = 100
    right = 150
    for i in range(4):
        # selenium 启动无页面浏览器
        driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', chrome_options=chrome_options)

        songsheet_num = count = 1
        songs_list = []
        datas = pd.read_csv('songsheets_rank/songsheets_us.csv').iloc[left:right, :]

        for link in datas['link']:
            get_songs_link(link.strip())

        # selenium 关闭无页面浏览器
        driver.close()

        songsheets_df = pd.DataFrame(songs_list, columns=['name', 'singer', 'link', 'comments_num'])
        if not os.path.isdir('output'):
            os.mkdir('output')
        songsheets_df.sort_values('comments_num', ascending=False).to_csv(f'output/songs_rank_0{i+3}.csv', sep=',', na_rep='NA')
        left += 50
        right +=50
