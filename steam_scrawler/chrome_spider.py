from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
urls = ["https://www.microsoft.com/en-us/p/fortnite-standard-founders-pack/bxwnx8st04js?activetab=pivot:reviewstabb"]

tot = []
counter = 0
def crawl(reviews_sec, counter):
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")  # define headless
    reviews = reviews_sec.find_elements_by_xpath("//div[@class = 'review cli_review']")
    ratings = reviews_sec.find_elements_by_xpath("//div[@class='review cli_review']/div/div[@class='c-rating f-user-rated f-individual']")
    headers = reviews_sec.find_elements_by_xpath("//div[@class='reviewFocusContainer']/div/h5")
    texts = reviews_sec.find_elements_by_xpath("//div[@class='c-content-toggle cli_reviews_content_toggle']/p")
    helpfuls = reviews_sec.find_elements_by_xpath("//div[@class='reviewFocusContainer']//p[@class='c-meta-text']")

    size = len(reviews)
    for i in range(size):
        id = reviews[i].get_attribute("data-review-id")
        rate = ratings[i].get_attribute("data-value")
        header = headers[i].get_attribute("aria-label")
        text = texts[i].text
        helpful = helpfuls[i].text
        tuple_row = {'review_id': id, 'star': rate, 'header': header, 'helpful': helpful, 'comment': text}
        tot.append(tuple_row)
    print("finish crawl ", counter)
for url in urls:
    browser = webdriver.Chrome()
    browser.get(url)
    browser.find_element_by_xpath("//a[@id='pivot-tab-ReviewsTab']").click()
    reviews_sec = browser.find_element_by_xpath("//div[@class='srv_reviews']")
    crawl(reviews_sec, 1)
    next_sec = reviews_sec.find_elements_by_xpath("//a[@class='c-glyph reviewsPageNext']")
    counter = 1
    while (next_sec):
        next_sec[0].click()
        time.sleep(random.uniform(0.5, 1))
        counter += 1
        try:
            crawl(browser, counter)
            next_sec = browser.find_elements_by_xpath("//a[@class='c-glyph reviewsPageNext']")
        except Exception as E:
            print("crawl end")
            json_str = json.dumps(tot)
            fileObject = open('testdata.json', 'w')
            fileObject.write(json_str)
            fileObject.close()
            browser.close()
    json_str = json.dumps(tot)
    fileObject = open('testdata.json', 'w')
    fileObject.write(json_str)
    fileObject.close()
    browser.close()