from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = 'http://weibo.com/ttarticle/p/show?id=2309404144228832806041'
web = webdriver.Firefox()
web.get(url)
try:
    element = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.ID, "articleRoot"))
    )
finally:
    html = web.page_source
    print(html)

    soup = BeautifulSoup(html, 'lxml')
    titles=soup.select('title')
    for i in titles:
        print(i.get_text())
    contents=soup.select('.WB_editor_iframe p')
    for i in contents:
        print(i.get_text())
    web.quit()
