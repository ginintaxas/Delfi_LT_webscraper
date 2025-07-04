from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options

def open_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")  
    service = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(options=options, service=service)
    driver.get("http://www.delfi.lt/")
    return driver

def check_correct_subdir(argSubdir):
    listofsubdirs["verslas", "sportas", "veidai"]
    for subdir in listofsubdirs:
        if subdir == argSubdir:
            return true
            break
    else:
        return false