from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Firefox()


def get_next_page():
    try:
        link = driver.find_element_by_link_text("下一页")
        link.click()
        print(driver.current_url)
    except NoSuchElementException:
        return 0


if __name__ == '__main__':
    driver.get('http://s.weibo.com/list/relpage?search=%25E6%2596%25B0%25E5%25B7%25A5%25E7%25A7%2591&limitType=article')
    while (True):
        num = get_next_page()
        if num == 0:
            break
