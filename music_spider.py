# -*- coding:utf-8 -*-

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import time


'''
函数功能：爬取网易云歌单信息
参数：
    url：起始url
    songsheets_list：歌单信息list
返回：
    无
'''
def get_songsheet_url(url, songsheets_list):
    global count
    global page

    # 无页面浏览器配置
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # selenium 请求url
    driver = webdriver.Chrome(executable_path='C:/Users/zhouxy/AppData/Local/Google/Chrome/Application/chromedriver.exe', chrome_options=chrome_options)
    driver.get(url)

    # 切换到frame标签
    driver.switch_to.frame('g_iframe')

    # 获取歌单信息
    songsheets = driver.find_elements_by_xpath('//*[@id="m-pl-container"]/*')
    print('=====' * 10, f'page[{page}]', '=====' * 10)
    for songsheet in songsheets:
        title = songsheet.find_element_by_xpath('div/a').get_attribute('title')
        link = songsheet.find_element_by_xpath('div/a').get_attribute('href')
        play_times = int(songsheet.find_element_by_xpath('div/div').text.replace('万', '0000'))
        creator = songsheet.find_element_by_xpath('p[2]/a').text
        songsheets_list.append([title, link, play_times, creator])
        print(f'[{count}] {title} {link} {play_times} {creator} done.')
        count += 1

    # 自动翻页
    next_page = driver.find_element_by_xpath('//*[@id="m-pl-pager"]/div/a[11]').get_attribute('href')
    if next_page != 'javascript:void(0)':
        driver.close()
        time.sleep(0.5)
        page += 1
        get_songsheet_url(next_page, songsheets_list)
    # driver.close()

if __name__ == '__main__':
    page = count = 1
    songsheets_list = []
    get_songsheet_url('https://music.163.com/#/discover/playlist/?cat=%E6%97%A5%E8%AF%AD', songsheets_list)
    songsheets_df = pd.DataFrame(songsheets_list, columns=['title', 'link', 'play_times', 'creator'])
    songsheets_df.sort_values('play_times', ascending=False).to_csv(f'songsheets.csv', sep=',', na_rep='NA')


