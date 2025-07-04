from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapper_functions import *

#opens a chromium browser with delfi.lt site
#!!!!!!!!!DONT FORGET TO driver.quit() AFTER USE!!!!!!!!!!!!!!!!!!
driver = open_driver()
with open("output.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)
driver.quit()