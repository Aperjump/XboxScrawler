import re

import os
import sys

import time

import json
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

maindriver = webdriver.Chrome()
url = "https://www.microsoft.com/en-us/store/top-paid/games/xbox"
maindriver.get(url)
while True:
    try:
        mainblock = maindriver.find_element_by_xpath("//ul[@class='m-pagination']")
        next_page = mainblock.find_element_by_xpath(".//a[@aria-label='next page']")
        next_page.click()
        urllist = maindriver.find_elements_by_xpath("//div[@class='m-channel-placement-item']")
        url_list = [i.find_element_by_xpath(".//a").get_attribute("href") for i in urllist]
    except NoSuchElementException as e:
        print("crawl finish")
        maindriver.close()
        break
