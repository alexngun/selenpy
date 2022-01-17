#%%
from selenpy.Crawler import BaseCrawler
from selenpy.Reader import Loader

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import re

class SelenpyCrawler(BaseCrawler):

    #table name
    collection = "data"
    #target domain
    domain = "https://www.amazon.com"
    #product display page pattern
    fURL = "https://www.amazon.com/dp/%s"
    #load a list of asins
    targets = Loader.read_pkl("config/tasks.pkl")

    def validateBlock(self, chrome):
        try:
            chrome.find_element(By.CSS_SELECTOR, 'form[action="/errors/validateCaptcha"]')
        except NoSuchElementException:
            return True
        else:
            return False

    def validatePage(self, chrome):
        try:
            #amazon displayed url not found error
            chrome.find_element(By.ID, 'g') 
        except NoSuchElementException:
            return True
        else:
            return False

    def validateTask(self, target):
        #verify that target is an asin
        if re.search(r"B[0-9A-Z]{9}", target):
            return True
        else:
            return False

    def spider(self, chrome, target):

        data = {"_id":target}

        #target data
        try:
            title = chrome.find_element(By.ID, "productTitle")
        except NoSuchElementException:
            data["title"] = None
        else:
            data["title"] = title.text

        return data

SPIDER = SelenpyCrawler