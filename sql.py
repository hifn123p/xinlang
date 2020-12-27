from selenium import webdriver
from bs4 import BeautifulSoup
import re
from pyquery import PyQuery
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from xinlang import db_conn, db_set

import pymysql

url2 = 'http://s.weibo.com/list/relpage?search=%25E6%2596%25B0%25E5%25B7%25A5%25E7%25A7%2591&limitType=article'

driver = webdriver.Firefox()


# 获取新浪搜索主页html
def web_open(url):
    driver.get(url)
    html = driver.page_source
    return html


# 获取新浪搜索页面文章的url
def get_urls(html):
    str = re.compile('<p class="link_title2"><a class="W_texta W_fb" href="(.*?)" title=', re.S)
    links = re.findall(str, html)
    return links


# 解析新浪文章，获取title content
def parse_url(url, cur,con):
    driver.get(url)
    global titles
    global contents
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "articleRoot"))
        )
        html = driver.page_source
        query = PyQuery(html)
        articles = query('.main_editor').items()
        for art in articles:
            title = art.find('.title').text()
            content = art.find('p').text()
            sql = "insert into article(title,content) values('%s', '%s');" % (title, content)
            cur.execute(sql)
            con.commit()
    except TimeoutException:
        None


# 获取下一页信息
def get_next_page():
    try:
        link = driver.find_element_by_link_text("下一页")
        link.click()
        html = driver.page_source
        return get_urls(html)
    except NoSuchElementException:
        return 0


def get_all_urls(url, cur,con):
    html = web_open(url)  # 打开新浪搜索
    list = get_urls(html)  # 正则匹配文章url
    while True:  # 循环每一页
        num = get_next_page()
        if num == 0:
            break;
        else:
            list.extend(num)

    for i in list:
        parse_url(i, cur,con)


if __name__ == '__main__':
    db_name = db_set.db_name.get('name')
    db_user = db_set.db_name.get('user')
    db_pass = db_set.db_name.get('password')
    db = 'new_e'
    # 建立数据库连接
    con = pymysql.connect(db_name, db_user, db_pass, db, charset='utf8')
    # 获取数据库游标
    cur = con.cursor()

    get_all_urls(url2, cur,con)
    driver.close()
    con.close()
