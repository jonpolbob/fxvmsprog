
from selenium import webdriver
import selenium

timeout = 120

def initwebwindows():

    # personalisation des options(rep de download et adresse vers chromdriver
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "c:/tmp"}
    options.add_experimental_option("prefs", prefs)
   # options.add_argument("headless");
    chromedriver = u"c:/windows/system32/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.set_page_load_timeout(timeout)
    return driver