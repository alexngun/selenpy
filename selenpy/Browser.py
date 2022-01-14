from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import json
import zipfile

from .common.variables import Mode
from .common.settings import PRIVATE_PROXY, BROWSER

class Chrome(webdriver.Chrome):

    def __init__(
            self, proxymanager, validate, type=Mode.LOCAL, headless=False, enable_image=True, 
            executable_path=Mode.DEFAULT, options=webdriver.ChromeOptions()
        ):

        self.proxyManger = proxymanager
        self.settings = BROWSER['options']
        self.type = type
        self.validate = validate
        self.executable_path = executable_path

        # ----------------------------- browser settings ----------------------------- #
        #go headless mode
        if headless:
            options.add_argument('--headless')

        #go imageless Mode
        if enable_image:
            options.add_argument('--blink-settings=imagesEnabled=false')

        #load all pre-defined browser settings
        for setting in self.settings:
            options.add_argument(setting)

        # ------------------------------ proxy settings ------------------------------ #
        #fetch one random proxy from the pool
        self.proxy = self.proxyManger.getProxy(type=self.type)
        #if proxy does require authentication
        if self.proxy != Mode.LOCAL and self.type == Mode.PRIVATE:

            authentication = PRIVATE_PROXY['background_js'] % (
                self.proxy.split(":")[0],
                self.proxy.split(":")[1],
                PRIVATE_PROXY['username'],
                PRIVATE_PROXY['password']
            )
            pluginfile = 'selenpy/dump/proxy_auth_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", PRIVATE_PROXY['manifest_json'])
                zp.writestr("background.js", authentication)
            options.add_extension(pluginfile)

        #if proxy does not require authentication
        elif self.proxy != Mode.LOCAL and self.type == Mode.DEFAULT:

            options.add_argument(f"--proxy-server={self.proxy}")

        options.add_argument(f'user-agent={UserAgent().random}')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        #boot chrome driver with all settings
        if self.executable_path == Mode.DEFAULT:
            super(Chrome, self).__init__(executable_path=ChromeDriverManager(log_level=0).install(), options=options)
        else:
            super(Chrome, self).__init__(executable_path=executable_path, options=options)

        #setup timeout settings
        self.implicitly_wait(BROWSER['elementTimeout'])
        self.set_page_load_timeout(BROWSER['browserTimeout'])

    def add_local_storage(self, key, value):
        self.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def get_local_storage(self):
        return self.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def get_shadow_root(self, driver, selector, tag):
        e = driver.find_element(selector, tag)
        shadowRootID = list(self.execute_script("return arguments[0].shadowRoot", e).values())[0]
        return WebElement(self, shadowRootID, w3c=True)

    def loadCookiesNlocalStorage(self):
        #setup cookie and local storage if any
        try:
            with open("config/cookies.json", "r") as f:
                cookies = json.load(f)
        except FileNotFoundError:
            pass
        else:
            for cookie in cookies:
                self.add_cookie(cookie)
        try:
            with open("config/local_storage.json", "r") as f:
                lstorage = json.load(f)
        except FileNotFoundError:
            pass
        else:
            for key in lstorage.keys():
                self.add_local_storage(key, lstorage[key])

    def get(self, *args, **kwargs):
        try:
            super(Chrome, self).get(*args, **kwargs)
        except TimeoutException:
            return False
        except WebDriverException:
            return False

        try:
            error = self.find_element_by_css_selector("div[class='error-code']")
        except NoSuchElementException:
            pass
        else:
            raise WebDriverException(error.text)

        return self.validate(self)

    def quit(self, *args, **kwargs):
        super(Chrome, self).quit(*args, **kwargs)
        self.proxyManger.releaseProxy(self.proxy)