from selenium import webdriver
from scrapper_functions import *
import sys
import time
try:
    #extracts config data from config.json file
    config_data = parse_json_config()
    #sets site subdir, output format and language based on the config file
    subdir = config_data["subdir"]
    language = config_data["language"]
    format = config_data["output"]["format"]
    output_file = config_data["output"]["file"]
    #opens a driver and sets driver subdir
    driver = open_driver()
    set_subdir(language, subdir, driver)
    #waits for JS generated content
    time.sleep(2)
    html = driver.page_source
    #parses and stores articles
    url_and_article_tuple = extract_article_list(html)
    title_list = url_and_article_tuple[0]
    full_content_url_list = url_and_article_tuple[1]
    full_content_text_list = parse_article_content_text(driver, full_content_url_list)
    store_articles(title_list, full_content_text_list, format, output_file)
finally:
    driver.quit()