from main import SPIDER
from selenpy.DBManger import MongoManger
from selenpy.formatoutput import Loader
import sys
import pandas as pd

if __name__ == '__main__':

    args = sys.argv

    command = args[1]

    if command == "start":
        
        start = None
        end = None
        headless = False
        threads = 4
        enable_image = False

        for arg in args:
            if "--headless" == arg :
                headless = True
            elif "-t" in arg[:2]:
                threads = int(arg[2:])
            elif "-b" in arg[:2]:
                start = int(arg[2:])
            elif "-e" in arg[:2]:
                end = int(arg[2:])
            elif "--enable_image" == arg:
                enable_image = True

        SPIDER(start=start, end=end, threads=threads, headless=headless, enable_image=enable_image).start()

    if command == "reset_proxy":
        db = MongoManger()
        db.proxy.resetProxies()

    if command == "output":
        table = args[2]
        db = MongoManger()
        loader = Loader()
        loader.start("Fetching data from db...")
        pd.DataFrame(db.get(table)).to_csv(table+".csv")
        loader.end("File has successfully output")