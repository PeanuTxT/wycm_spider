# -*- coding:utf-8 -*-

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium import webdriver
import pandas as pd
import time

'''
函数功能：爬取网易云歌单信息
参数：
    url：起始url
返回：
    无
'''
def get_songsheet_data(url):
    global count

    # selenium 请求url
    driver.get(url)
    print(f'url:{url}')

    # 切换到frame标签
    driver.switch_to.frame('g_iframe')

    # 歌单信息
    title = driver.find_element_by_xpath('//div[@class="hd f-cb"]/div/h2').text
    play_times = int(driver.find_element_by_xpath('//*[@id="play-count"]').text)
    collection_times = int(driver.find_element_by_xpath('//*[@id="content-operation"]/a[3]/i').text.replace('万', '0000')[1:-1])
    if driver.find_element_by_xpath('//*[@id="content-operation"]/a[4]/i').text == '分享':
        relay_times = 0
    else:
        relay_times = int(driver.find_element_by_xpath('//*[@id="content-operation"]/a[4]/i').text[1:-1])
    if driver.find_element_by_xpath('//*[@id="cnt_comment_count"]').text == '评论':
        comments = 0
    else:
        comments = int(driver.find_element_by_xpath('//*[@id="cnt_comment_count"]').text)
    creator = driver.find_element_by_xpath('//div[@class="user f-cb"]/span/a').text
    create_date = driver.find_element_by_xpath('//div[@class="user f-cb"]/span[2]').text.split(' ')[0]

    songsheets_list.append([title, url, play_times, collection_times, relay_times, comments, creator, create_date])
    print(f'[{count}] ', title, url, play_times, collection_times, relay_times, comments, creator, create_date, 'done.')
    count += 1


if __name__ == '__main__':

    # 无页面浏览器配置
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(UserAgent().random)
    chrome_options.add_argument(f'--proxy-server=http://113.121.146.222:5649')

    # 修改selenium页面加载策略
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    # selenium 启动无页面浏览器
    driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', chrome_options=chrome_options)

    page = count = 1
    songsheets_list = []
    with open('link_list_ds.txt', 'r') as f:
        for link in f.readlines():
            get_songsheet_data(link)
            time.sleep(0.5)

    # selenium 关闭无页面浏览器
    driver.close()

    songsheets_df = pd.DataFrame(songsheets_list, columns=['title', 'link', 'play_times', 'collection_times',
                                                           'relay_times', 'comments', 'creator', 'create_date'])
    songsheets_df.sort_values('collection_times', ascending=False).to_csv(f'songsheets_rank/songsheets_ds.csv', sep=',', na_rep='NA')


