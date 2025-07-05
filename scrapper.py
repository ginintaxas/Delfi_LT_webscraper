from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapper_functions import *
import sys
import time
try:
    subdir = sys.argv[1]
    driver = open_driver()
    set_subdir(subdir, driver)
    time.sleep(2)
    html = driver.page_source
    article_list = parse_html(html)
    store_articles_in_csv(article_list)
finally:
    driver.quit()