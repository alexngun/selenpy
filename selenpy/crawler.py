#%%
from .common.settings import BROWSER, LOGGER
from .common.variables import Mode
from .DBManger import MongoManger
from .formatoutput import Loader
from .Browser import Chrome

from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor
from abc import abstractmethod
import time
import os

from pymongo.errors import DuplicateKeyError

init(autoreset=True)

#%%
class BaseCrawler():

    collection = "untitled"
    chromes = []
    cookies = []
    targets = []
    proxy = None
    domain = None
    fURL = "%s"

    log_source = False
    
    class Proxy:
        proxies = None
        type = Mode.LOCAL

    def __init__(self, start=None, end=None, threads=4, headless=False, enable_image=False):

        self.db = MongoManger()
        self.loader = Loader()

        self.threads = threads
        self.headless = headless
        self.enable_image = enable_image

        for _ in range(threads):
            self.chromes.append(None)

        self.loader.start("Initiazling Tasks...")

        os.environ['WDM_LOG_LEVEL'] = '0'

        # ------------------------ eliminate duplicate targets ----------------------- #
        targets = list(set(self.targets))
        self.total = len(targets)

        done = []
        logged = self.db.get(col=self.collection, column={"_id":1})
        errored = self.db.get(col=f'{LOGGER}-{self.collection}', column={"_id":1})
        for doc in logged:
            done.append(doc['_id'])
        for doc in errored:
            done.append(doc['_id'])

        # -------------------------------- slice tasks ------------------------------- #
        self.targets = list(set(targets[start:end])-set(done))
        self.tasks_num = len(self.targets)
        self.loader.end(f"✅ Initializaion completed - {self.tasks_num} of {self.total} new tasks were pushed to the pool.\n")
        print(f"\r☕ {self.total - self.tasks_num} records found in database")
        # ------------------------------- load proxies ------------------------------- #

        if self.Proxy.proxies:
            self.db.proxy.loadProxy(self.Proxy.proxies, self.Proxy.type)
            size = len(self.db.get("proxy", filter={"status":"A", "type":self.Proxy.type}))
            print(f"💻 {size} proxies currently available")

    @abstractmethod
    def spider(self, chrome, target):
        '''
            Abstract method
            input: selenium-browser object
            output: data (dictionary object)
        '''
        raise NotImplementedError("Please implement a 'spider' method!")

    def __crawl(self, thread):

        if len(self.targets) > 0:
            time.sleep(thread * 0.6)
            self.chromes[thread] = self.startChrome(thread)

            while len(self.targets) > 0:

                target = self.targets.pop(0)

                num = self.db.count(self.collection) + self.db.count(f'{LOGGER}-{self.collection}')
                self.loader.displayProgress(num, self.total, 
                    f"⏳ Thread {thread+1} -> {target} ({self.chromes[thread].proxy}) "
                )

                if not self.validateTask(target):
                    self.logError(target, f'InvalidTaskPattern: {target}')
                    continue
                
                if self.db.exists(self.collection, target):
                    continue

                if self.db.exists(f"{LOGGER}-{self.collection}", target):
                    continue

                while True:

                    if self.chromes[thread].get(url=self.fURL % target ):
                        break
                    else:
                        self.chromes[thread].quit()

                        if self.chromes[thread].proxy == Mode.LOCAL:
                            time.sleep(BROWSER['waitInterval'])

                        self.chromes[thread] = self.startChrome(thread)

                time.sleep(BROWSER['delay'])

                if not self.validatePage(self.chromes[thread]):
                    self.logError(target, f'PageNotFound: {self.fURL % target}')
                    continue

                if self.log_source:
                    self.db(f"{self.collection}-source", {
                        "_id":target,
                        "page":self.chromes[thread].page_source
                    })

                data = self.spider(self.chromes[thread], target)
                self.db.insert(self.collection, data)
            
    def startChrome(self, thread):

        while True:
            num = self.db.count(self.collection) + self.db.count(f'{LOGGER}-{self.collection}')
            self.loader.displayProgress(num, self.total, f'⏳ Thread {thread+1} -> starting chrome ')
            chrome = Chrome (
                validate=self.validateBlock, proxymanager=self.db.proxy,
                type=self.Proxy.type, headless=self.headless, enable_image=self.enable_image
            )
            if chrome.get(self.domain):
                chrome.loadCookiesNlocalStorage()
                return chrome
            else:
                chrome.quit()
                if chrome.proxy == Mode.LOCAL:
                    time.sleep(BROWSER['waitInterval'])

    def logError(self, id, message):
        try:
            self.db.insert(f'{LOGGER}-{self.collection}', {
                '_id':id,
                'error':message
            })
        except DuplicateKeyError:
            pass

    def start(self):

        time.sleep(1)
        self.loader.indicateLoading()

        if self.threads == 1 or len(self.targets) < self.threads:
            self.__crawl(thread=0)
        else:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                for thread in range(self.threads):
                    executor.submit(self.__crawl, thread)

        num = self.db.count(self.collection) + self.db.count(f'{LOGGER}-{self.collection}')
        self.loader.end(Style.DIM + Fore.CYAN + f"✅ All Done - total number of {num} tasks were fetched")

    def validateBlock(self, chrome):
        return True

    def validateTask(self, target):
        return True

    def validatePage(self, chrome):
        return True
