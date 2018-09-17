from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
urls = ["https://www.microsoft.com/en-us/p/fortnite-standard-founders-pack/bxwnx8st04js?activetab=pivot:reviewstabb"]

tot = []
def crawl(url):
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")  # define headless
    browser = webdriver.Chrome()
    browser.get(url)
    browser.find_element_by_xpath("//a[@id='pivot-tab-ReviewsTab']").click()
    reviews_sec = browser.find_element_by_xpath("//div[@class='srv_reviews']")
    reviews = reviews_sec.find_elements_by_class_name("review")
    for review_iter in reviews:
        id = review_iter.get_attribute("data-review-id")
        text = review_iter.find_elements_by_xpath("//div[@class='c-rating f-user-rated f-individual']").get_attribute("data-value")
    time.sleep(3)
    a = 3
    browser.close()
    return a
for url in urls:
    crawl(url)
