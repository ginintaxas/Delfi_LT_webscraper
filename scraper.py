from selenium import webdriver
from utils import *
import sys
import time
try:
    config_data = parse_json_config()
    subdir = config_data["subdir"]
    language = config_data["language"]
    format = config_data["output"]["format"]
    output_file = config_data["output"]["file"]
    driver = open_driver()
    set_subdir(language, subdir, driver)
    #waits for JS generated content
    time.sleep(2)
    html = driver.page_source
    #parses and stores articles
    url_and_article_tuple = extract_article_list(html)
    title_list = url_and_article_tuple[0]
    full_content_url_list = url_and_article_tuple[1]
    store_articles(title_list, full_content_url_list, format, output_file)
finally:
    driver.quit()