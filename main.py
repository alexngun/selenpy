#%%
from selenpy.Crawler import BaseCrawler
from selenpy.common.variables import Mode
from selenpy.Reader import Loader

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class SelenpyCrawler(BaseCrawler):

    collection = "data"
    domain = "https://www.amazon.com"
    targets = []

    def validateBlock(self, chrome):
        #implement a method to response to target server block
        return True

    def validatePage(self, chrome):
        #implement a method to response to invalid page
        return True

    def validateTask(self, target):
        #implement a method to response to invalid target pattern
        return True

    def spider(self, chrome, target):

        data = {"_id":target}

        #implement your script here

        return data

SPIDER = SelenpyCrawler

# %%
