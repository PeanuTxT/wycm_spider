# -*- coding:utf-8 -*-

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import time
import json

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent


'''
函数功能：爬取网易云歌单信息
参数：
    url：起始url
返回：
    无
'''
def get_songsheet_url(url):
    global page
    global link_txt

    # selenium 请求url
    driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', chrome_options=chrome_options)
    driver.get(url)

    # 切换到frame标签
    driver.switch_to.frame('g_iframe')

    # 获取歌单link
    songsheets = driver.find_elements_by_xpath('//*[@id="m-pl-container"]/*')
    print('=====' * 10, f'page[{page}]', '=====' * 10)
    for songsheet in songsheets:
        link = songsheet.find_element_by_xpath('div/a').get_attribute('href')
        link_txt += link + '\n'
        # get_song_url(link)

    # 自动翻页
    next_page = driver.find_element_by_xpath('//*[@id="m-pl-pager"]/div/a[11]').get_attribute('href')
    if next_page != 'javascript:void(0)':
        driver.close()
        time.sleep(0.5)
        page += 1
        get_songsheet_url(next_page)
    # driver.close()

def get_song_url(url):
    global count

    # selenium 请求url
    # driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', chrome_options=chrome_options)
    driver = webdriver.Chrome(
        executable_path='C:/Users/zhouxy/AppData/Local/Google/Chrome/Application/chromedriver.exe',
        chrome_options=chrome_options)

    driver.get(url)
    print(f'url:{url}')

    # 切换到frame标签
    driver.switch_to.frame('g_iframe')

    # 歌单信息
    title = driver.find_element_by_xpath('//div[@class="hd f-cb"]/div/h2').text
    play_times = int(driver.find_element_by_xpath('//*[@id="play-count"]').text)
    collection_times = int(driver.find_element_by_xpath('//*[@id="content-operation"]/a[3]/i').text.replace('万', '0000')[1:-1])
    relay_times = int(driver.find_element_by_xpath('//*[@id="content-operation"]/a[4]/i').text[1:-1])
    comments = int(driver.find_element_by_xpath('//*[@id="cnt_comment_count"]').text)
    creator = driver.find_element_by_xpath('//div[@class="user f-cb"]/span/a').text
    create_date = driver.find_element_by_xpath('//div[@class="user f-cb"]/span[2]').text.split(' ')[0]

    songsheets_list.append([title, url, play_times, collection_times, relay_times, comments, creator, create_date])
    print(f'[{count}] ', title, url, play_times, collection_times, relay_times, comments, creator, create_date, 'done.')
    count += 1

    driver.close()


if __name__ == '__main__':
    # ip = json.loads(requests.get('http://daili.spbeen.com/get_api_json?token=d9RHl6r5iCCVgyVD9jR6fnSo&num=1').text)['data'][0]
    # print(ip)
    # 无页面浏览器配置
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(UserAgent().random)
    chrome_options.add_argument(f'--proxy-server=http://119.101.116.127:9999')

    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

    page = count = 1
    link_txt = ''
    get_songsheet_url('https://music.163.com/#/discover/playlist/?cat=%E6%AC%A7%E7%BE%8E')
    # with open('link_list.txt', 'w') as f:
    #     f.write(link_txt)

    # songsheets_list = []
    # with open('link_list.txt', 'r') as f:
    #     for link in f.readlines():
    #         get_song_url(link)
    #         time.sleep(0.5)
    #
    # songsheets_df = pd.DataFrame(songsheets_list, columns=['title', 'play_times', 'link', 'collection_times',
    #                                                        'relay_times', 'comments', 'creator', 'create_date'])
    # songsheets_df.sort_values('comments', ascending=False).to_csv(f'songsheets.csv', sep=',', na_rep='NA')


