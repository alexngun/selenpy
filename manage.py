from main import SPIDER
import sys

if __name__ == '__main__':

    args = sys.argv

    command = args[1]

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

    if command == "start":
        SPIDER(start=start, end=end, threads=threads, headless=headless, enable_image=enable_image).start()
