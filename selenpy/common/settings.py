DATABASE = {
    'host': '192.168.2.94',
    'port': '27017',
    'username': None, #'data'
    'password': None, #'cafl-2021'
    'db': 'test'
}

BROWSER = {
    #broswer settings
    'options': [
        "--no-sandbox",
        "--dns-prefetch-disable",
        "--disable-browser-side-navigation",
        "--disable-dev-shm-usage",
        "--disable-infobars",
        "enable-automation"
    ],
    #delay,
    'delay':0,
    #waiting time to restart chrome after blocked by Amazon
    'waitInterval': 10,
    #wait for web element
    'elementTimeout': 0.5,
    #browser loading timeout
    'browserTimeout': 180,
}

LOGGER = "error"

VERBOSEDIGIT = 2

PROGRESSLEN = 25

PRIVATE_PROXY = {
# -------------- private proxy with authentication configuration ------------- #
    # 'username': '12345678',
    # 'password': '12345678',
    "manifest_json": """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
    """,
    "background_js": """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
    """ 
}