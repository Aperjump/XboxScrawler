from selenium import webdriver
import multiprocessing as mp
from functools import partial
from node_crawler import webcrawl,webdrivers
import time
class Chromepool(object):

    def __init__(self, num):
        self.poolnum = num
        self.webdrivers = webdrivers
        self.manager = mp.Manager()
        self.freeque = self.manager.Queue()
        for i in range(self.poolnum):
            self.freeque.put(i)
        print("create chrome number is " + str(len(self.webdrivers)))

    def __del__(self):
        print("finish crawl")

        #for i in range(self.poolnum):
        #   self.webdrivers[i].close()

    def givenewtask(self, url):
        if not self.freeque.empty():
            chrome_index = self.freeque.get()
            print("pass url " + url + " for " + str(chrome_index))
            new_p = mp.Process(target = webcrawl, args = (chrome_index, url, self.freeque, ))
            new_p.start()
            return True
        else:
            return False

if __name__ == "__main__":
    chrome_test = Chromepool(2)
    urls = ["https://www.microsoft.com/en-us/p/fallout-76/bx3dspqpvnqr?cid=msft_web_chart",
            "https://www.microsoft.com/en-us/p/red-dead-redemption-2/bpswgqbw7r3g?cid=msft_web_chart",
            "https://www.microsoft.com/en-us/p/call-of-duty-black-ops-4/c19n0723phfl?cid=msft_web_chart",
            "https://www.microsoft.com/en-us/p/nba-2k19/bnw34b7v705c?cid=msft_web_chart&activetab=pivot:overviewtab"]
    for url in urls:
        while not chrome_test.givenewtask(url):
            time.sleep(10)
            pass
