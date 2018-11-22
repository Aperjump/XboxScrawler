# import scrapy
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from chromepool import Chromepool

class FortnightCrawler():
    name = 'Fortnight'
    tot_list = []

    def __init__(self):
        # use any browser you wish
        self.maindriver = webdriver.Chrome()
        self.driverpool = Chromepool(5)

    def __del__(self):
        del self.driverpool
        #self.maindriver.close()

    def start_requests(self):
        url = "https://www.microsoft.com/en-us/store/top-paid/games/xbox"
        self.maindriver.get(url)
        self.maindriver.refresh()
        while True:
            ads = self.maindriver.find_element_by_xpath("//div[@class='sfw-dialog']")
            tab_index = ads.get_attribute("tabindex")
            if tab_index == '0':
                ads_close = ads.find_element_by_xpath(".//div[@class='c-glyph glyph-cancel']")
                ads_close.click()

            urllist = self.parseurl()
            for gameurl in urllist:
                print ("assign " + gameurl)
                while not self.driverpool.givenewtask(gameurl):
                    time.sleep(10)

            mainblock = self.maindriver.find_element_by_xpath("//ul[@class='m-pagination']")
            for _ in range(3):
                try:
                    next_page = mainblock.find_element_by_xpath(".//a[@aria-label='next page']")
                    print("#######NEXT_PAGE###########")
                    next_page.click()
                    break
                except NoSuchElementException as e:
                    print("crawl finish")
                    self.maindriver.close()
                    break
                except:
                    pass

    def parseurl(self):
        Eurl_list = self.maindriver.find_elements_by_xpath("//div[@class='m-channel-placement-item']")
        return [i.find_element_by_xpath(".//a").get_attribute("href") for i in Eurl_list]



if __name__ == "__main__":
    test_crawler = FortnightCrawler()
    test_crawler.start_requests()