from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
#opens a chromium browser with delfi.lt site
#!!!!!!!!!DONT FORGET TO driver.quit() AFTER USE!!!!!!!!!!!!!!!!!!
def open_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")  
    service = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://www.delfi.lt/")
    return driver
#check if the selected subdir for delfi.lt is available for scraping NOT IN USE YET
def check_correct_subdir(argSubdir):
    listofsubdirs = ["verslas", "sportas", "veidai"]
    for subdir in listofsubdirs:
        if subdir == argSubdir:
            return True
            break
    else:
        return False
#--------------------------------------------------------------------------------------- 

def store_articles_in_csv(article_list):
    with open("articles.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for val in article_list:
            writer.writerow([val])

def strip_of_hashtags_and_quotes(text):
    if text.startswith('#'):
        space_index = text.find(' ')
        if space_index != -1:
            text = text[space_index+1:]
    if text.endswith('"') and text.startswith('"'):
        text = text[1:-1]
    print(text)
    return text

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('article')
    article_list = []
    for article in articles:
        h5tag = article.find("h5")
        article_text = h5tag.get_text(strip=True)
        article_text = strip_of_hashtags_and_quotes(article_text)
        article_list.append(article_text)
    return article_list