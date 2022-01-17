# Selenpy

<p>
    <img src="https://cdn.icon-icons.com/icons2/2415/PNG/512/mongodb_original_wordmark_logo_icon_146425.png" width="60">
    <img src="https://i.imgur.com/MdFMJ5h.png" width="150">
</p>


This framework is built on top of Selenium providing the nesscary features to make web crawling more efficiency and easy.
- supports as many threadings as machines can handle
- distributed web crawling design for machines scaling 
- proxy auto rotation (private proxies are also supported)
- automating error detection (block, format check, etc)
- cookies and local storage insertion
- pause and start from where you left off
- supports browser extension

### Why Selenpy?

Selenium mimics what an actual human would do to browse a website. It increases the difficulties for target websites to detect a crawling robot. Traditional web scraping can only crawl static page. However, with Selenium dynamic page scraping is also possible.

### User Manual

#### Get Started

`/selenpy/common.settings`

Modify the config file to connect to your own db server
```python
DATABASE = {
    'host': '000.000.0.00', #your mongodb address
    'port': '00000', #your mongodb address port
    'username': None, #database username if any
    'password': None, #database password if any
    'db': 'mydb' #select a databse
}

```

`/main.py`

Define a class extending from `BaseCrawler` class (* are required properties)

Below is the variables that can be specified

| variables      | Description | type    |
| :---           |    :----   |          :--- |
| `collection` *    | table name to be stored in database | `str`  |
| `domain` *  | target website domain        | `str`    |
| `targets` *  | targets id/urls        | `array`     |
| `fURL`   | url pattern        |  `format str`     |
| `log_source`   | save the entire html souce    |  `boolean`     |
| `Proxy`   | use proxies if specified   |  `class`     |

Below is the methods that can be specified

| variables      | Description | input    | output  |
| :---           | :----   | :--- | :---  |
| `spider` *   | page scraping script  |  `SeleniumWebElement` | `dict` |
| `validateBlock` | validate whether the browser is blocked by target server | `SeleniumWebElement` | `boolean` |
| `validatePage` | validate whether the page is displaying correct content | `SeleniumWebElement` | `boolean` |
| `validateTask` | validate whether task is in correct format | `str` | `boolean` |

For more details, please find an example in `demo.py` for Amazon products crawling.

#### Proxy
For setting up proxy, please define a class named as `Proxy` inside your own crawler class.
```python
    from selenpy.Crawler import BaseCrawler
    from selenpy.common.variables import Mode
    from selenpy.Reader import Loader

    class MyCrawlerClass(BaseCrawler):

        ...

        class Proxy:
            proxies = Loader.read_json("<your_proxies_location>.json")
            type = Mode.DEFAULT #public proxy

        ...

```

`proxies` should be a `list` with the following naming convention 
(host is a required property while region is optional)

```json
[
    {"host":"888.88.88.888:23056", "region":"Boca Raton Florida"},
    {"host":"111.11.111.111:23056", "region":"Boston Massachusetts"},
    ...
]
```
If you are using private proxy, you need to specify `type = Mode.PRIVATE` instead. 
You would also need to modify the config file.
`/selenpy/common.settings`
```python
PRIVATE_PROXY = {
    'username': '12345678',
    'password': '12345678',
    ...
```

#### Run Script
type `python manage.py start` in your termianl to start crawling. Below are some extra arguments.
| options      | Description | Default |
| :---           |    :----   | :---- |
| `--headless`   | browser headless mode | `False` |
| `-t{}` | number of threads assigned for the task    | `4` |
| `-b{}`  | slice tasks (begining index)     | `0` |
| `-e{}` | slice tasks (ending index)  | `end` |
| `--enable_image` | hide image | `True` |
