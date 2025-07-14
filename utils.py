from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import json
import sqlite3
def open_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")  
    service = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(options=options, service=service)
    return driver

def valid_language(language):
    if language == 'lt' or language == 'ru' or language == 'en':
        return True
    else:
        return False

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

def set_subdir(language, subdir, driver):
    if check_correct_subdir(language, subdir):
        if language == 'lt':
            driver.get(f"https://www.delfi.lt/{subdir}")
        else:
            driver.get(f"https://www.delfi.lt/{language}/{subdir}")
    else:
        driver.get("https://www.delfi.lt/")
        raise Exception(f"No subdir under name {subdir} is not yet available to scrape or incorrect language")

def store_sql(article_list, output_path):
    article_list_tuples = []
    for article in article_list:
        article_list_tuples.append((article,))
    con = sqlite3.connect(output_path)
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
    """)
    cursor.executemany("INSERT INTO articles (title) VALUES (?)", article_list_tuples)
    con.commit()

# stores in text format but with full article content !!! REQUIRES output file to be a folder
def txt_full_store(title_list, article_list, output_folder):
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    for id, title in enumerate(title_list):
        if id >= len(article_list):
            break
        with open(output_path / f"{id}.txt", mode="w", newline="", encoding="utf-8") as file:
            file.write(title+"\n")
            file.write(article_list[id])
#stores a list of articles in the given format
def store_articles(title_list, article_url_list, format, output):
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if format == "csv":
        with open(output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for article in title_list:
                writer.writerow([article])
    if format == "txt":
        with open(output_path, mode="w", encoding="utf-8") as file:
            for article in title_list:
                file.write(article+'\n')
    if format == "sqlite":
        store_sql(title_list, output_path)
    if format == "txt_full":
        article_content_list = parse_article_content_text(driver, full_content_url_list)
        txt_full_store(title_list, article_content_list, output_path)
def strip_of_hashtags_and_quotes(text):
    if text.startswith('#'):
        space_index = text.find(' ')
        if space_index != -1:
            text = text[space_index+1:]
    if text.endswith('"') and text.startswith('"'):
        text = text[1:-1]
    return text

#return a tuple of which first member is title list and the second one is article url list for parsing
def extract_article_list(html):
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('article')
    article_list = []
    url_list = []
    for article in articles:
        url_list.append(extract_article_content_url(article))
        h5tag = article.find("h5")
        article_text = h5tag.get_text(strip=True)
        article_text = strip_of_hashtags_and_quotes(article_text)
        article_list.append(article_text)
    return (article_list, url_list)
#finds the correct href atribute for the full article text url
def extract_article_content_url(article_html):
    divOfUrl = article_html.find("div").find("div")
    url = divOfUrl.find("a").get("href")
    httpPrefix = "https://www.delfi.lt"
    if not url.startswith(httpPrefix):
        url = httpPrefix + url
    return url
#parses the full article which is located in a subdir of delfi
def parse_article_content_text(driver, url_list):
    article_text_list = []
    for url in url_list:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        #finds the article text section
        article_block = soup.find('div', class_="col-article")
        if article_block == None:
            article_text_list.append('empty or failed to fetch')
            continue
        full_text = ""
        p_tags = article_block.find_all('p')
        #extracts the text from the article
        for p in p_tags:
            text = p.find(text=True, recursive=False)
            #if the text value is null (none) then make it an empty string
            text = text.strip() if text else ''
            full_text = full_text + '\n' + text
        article_text_list.append(full_text)
    return article_text_list
def parse_json_config():
    with open('config.json', 'r') as file:
        config_data = json.load(file)
        return config_data