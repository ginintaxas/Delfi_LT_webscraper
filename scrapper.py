from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapper_functions import *
import time
try:
    driver = open_driver()
    time.sleep(2)
    html = driver.page_source
    article_list = parse_html(html)
    store_articles_in_csv(article_list)
finally:
    driver.quit()