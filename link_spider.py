# -*- coding:utf-8 -*-

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium import webdriver
import time


'''
函数功能：爬取网易云歌单url
参数：
    url：起始url
返回：
    无
'''
def get_songsheet_url(url):
    global page
    global link_txt

    # selenium 请求url
    driver.get(url)

    # 切换到frame标签
    driver.switch_to.frame('g_iframe')

    # 获取歌单link
    songsheets = driver.find_elements_by_xpath('//*[@id="m-pl-container"]/*')
    print('=====' * 10, f'page[{page}]', '=====' * 10)
    for songsheet in songsheets:
        link = songsheet.find_element_by_xpath('div/a').get_attribute('href')
        link_txt += link + '\n'

    # 自动翻页
    next_page = driver.find_element_by_xpath('//*[@id="m-pl-pager"]/div/a[11]').get_attribute('href')
    if next_page != 'javascript:void(0)':
        time.sleep(0.5)
        page += 1
        get_songsheet_url(next_page)


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
    link_txt = ''
    get_songsheet_url('https://music.163.com/#/discover/playlist/?cat=%E7%94%B5%E5%AD%90')

    # selenium 关闭无页面浏览器
    driver.close()

    with open('link_list_ds.txt', 'w') as f:
        f.write(link_txt)
