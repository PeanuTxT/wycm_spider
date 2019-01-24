# -*- coding:utf-8 -*-

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium import webdriver
import pandas as pd

def get_songs_data(url):
    global count

    # selenium 请求url
    driver.get(url)
    print(f'url:{url}')

    # 切换到frame标签
    driver.switch_to.frame('g_iframe')

    # 歌单信息
    songsheets = driver.find_element_by_xpath('//tbody')
    title = songsheets.find_element_by_xpath('tr/td[2]/div/div/div/span/a/b').text.replace('/&nbsp;/g', '')

    songs_list.append([])
    print(f'[{count}] ', title, 'done.')
    count += 1

if __name__ == '__main__':

    # 无页面浏览器配置
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(UserAgent().random)
    chrome_options.add_argument(f'--proxy-server=http://113.231.199.122:4237')

    # 修改selenium页面加载策略
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    # selenium 启动无页面浏览器
    driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', chrome_options=chrome_options)

    page = count = 1
    songs_list = []
    datas = pd.read_csv('songsheets_rank/songsheets_us.csv')
    for link in datas['link']:
        get_songs_data(link.strip())
        break

    # selenium 关闭无页面浏览器
    driver.close()

