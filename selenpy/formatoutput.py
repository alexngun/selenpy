#%%
import time
import sys
import itertools
import threading
from .common.settings import VERBOSEDIGIT, PROGRESSLEN

#%%
class Loader():

    done = False
    current = ""

    def __animate(self, message):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            sys.stdout.write(f'\r{message} ' + c + '                       ')
            sys.stdout.flush()
            time.sleep(0.1)

    def __animateEnd(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            sys.stdout.write(f'\r{self.current} ' + c + '                       ')
            time.sleep(0.1)
        
    def start(self, message):
        self.done = False
        threading.Thread(target=self.__animate, args=(message,)).start()

    def indicateLoading(self):
        self.done = False
        threading.Thread(target=self.__animateEnd).start()

    def end(self, complete):
        self.done = True
        sys.stdout.write(f'\r{complete}                                                    ')

    def displayProgress(self, current, total, message="", showBar=False):
        p = round((current / (total-1) ) * 100 , VERBOSEDIGIT)
        barLen = int(PROGRESSLEN * (p/100))
        if showBar:
            bar = f"{message}|"
            for _ in range(barLen):
                bar += "█"
            for _ in range(PROGRESSLEN-barLen):
                bar += " "
            bar += f"| {p} %"
        else:
            bar = f"{message}| {p} %"
        self.current = bar
