from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import json
#opens a chromium browser with delfi.lt site
#!!!!!!!!!DONT FORGET TO driver.quit() AFTER USE!!!!!!!!!!!!!!!!!!
def open_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")  
    service = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(options=options, service=service)
    return driver

#checks if the selected language is valid
def valid_language(language):
    if language == 'lt' or language == 'ru' or language == 'en':
        return True
    else:
        return False

#check if the selected subdir for delfi.lt is available for scraping
def check_correct_subdir(language, argSubdir):
    if valid_language(language):
        listofLTsubdirs = ["tv", "laisvalaikis", "verslas", "sportas", "veidai", ""]
        listofENsubdirs = ["politics", "business", "world-lithuanians", "expats-in-lt", "culture", "lifestyle", ""]
        listofRUsubdirs = ["poslednie", "news/economy, detektor-lzhi","sport", "misc", ""]
        if language == "lt":
            return argSubdir in listofLTsubdirs
        elif language == "en":
            return argSubdir in listofENsubdirs
        else:
            return argSubdir in listofRUsubdirs

#sets the selected subdir of the website, example: delfi.lt/verslas
def set_subdir(language, subdir, driver):
    if check_correct_subdir(language, subdir):
        if language == 'lt':
            driver.get(f"https://www.delfi.lt/{subdir}")
        else:
            driver.get(f"https://www.delfi.lt/{language}/{subdir}")
    else:
        driver.get("https://www.delfi.lt/")
        raise Exception(f"No subdir under name {subdir} is not yet available to scrape or incorrect language")

#stores a list of articles in csv format
def store_articles(article_list, format, output):
    #creates an output folder if it doesnt exist
    output_path = Path(f"{output}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if format == "csv":
        with open(output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for article in article_list:
                writer.writerow([article])
    if format == "txt":
        with open(output_path, mode="w", encoding="utf-8") as file:
            for article in article_list:
                file.write(article+'\n')

#strips of unnesecarry info
def strip_of_hashtags_and_quotes(text):
    if text.startswith('#'):
        space_index = text.find(' ')
        if space_index != -1:
            text = text[space_index+1:]
    if text.endswith('"') and text.startswith('"'):
        text = text[1:-1]
    return text

#return a list of articles from given html
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
#parses the config.json file and returns language and subdir
def parse_json_config():
    with open('config.json', 'r') as file:
        config_data = json.load(file)
        return config_data