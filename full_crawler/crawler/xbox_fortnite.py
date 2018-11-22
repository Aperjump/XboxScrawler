# python3
import re

import os
import sys

import time

import json
import random

from selenium import webdriver


def next_page():
    for _ in range(3):
        try:
            next_page_button = browser.find_element_by_xpath("//div[@class = 'context-pagination']").find_elements_by_tag_name("li")[1]
            next_page_button.click()
            break
        except:
            pass
    # for _ in range(3):
    #     try:
    #         browser.find_element_by_xpath("//div[@class='review cli_review']")
    #         break
    #     except:
    #         time.sleep(2)
            # browser.find_element_by_xpath("//div[@class = 'context-pagination']").find_elements_by_tag_name("li")[1].click()




def get_info(r):

    right_box = r.find_element_by_xpath(".//div[@data-grid = 'col-3']")

    star_rate = right_box.find_element_by_xpath(".//div[@class = 'c-rating f-user-rated f-individual']").get_attribute('data-value')
    try:
        device = right_box.find_element_by_xpath(".//p[@class = 'c-meta-text']").text
    except:
        device = 'unknown'

    comment_meta = right_box.find_elements_by_xpath(".//p[@class = 'c-paragraph-3']")
    date = comment_meta[0].text
    userID = comment_meta[1].text


    left_box = r.find_element_by_xpath(".//div[@data-grid = 'col-9']/div")
    head = left_box.find_element_by_tag_name('h5').text

    review_area = left_box.find_element_by_xpath(".//div[@class='c-content-toggle cli_reviews_content_toggle']")
    # see if it has the "more" button to click and expand
    button = review_area.find_element_by_tag_name("button")
    if button.get_attribute('style') == 'display: none;':
        review_text = review_area.find_element_by_tag_name('p').text
    else:
        button.click()
        # time.sleep(1)
        dialog_box = browser.find_element_by_id('review-comment-dialog')
        review_text = dialog_box.find_element_by_xpath(".//div[@role = 'dialog']//p[@class = 'c-paragraph']").text
        # time.sleep(0.5)

        # to counter situation where element is not visible
        for _ in range(3):
            try:
                close_dialog_button = dialog_box.find_element_by_tag_name('button')
                close_dialog_button.click()
                break
            except:
                # time.sleep(0.5)
                pass



    buttom_box = r.find_element_by_xpath(".//div[@data-grid = 'col-12']")
    helpfulness = buttom_box.find_element_by_tag_name('p').text

    if helpfulness != "":
        try:
            helpful_num, total_num = re.search('([0-9,]*) out of ([0-9,]*)',helpfulness).group(1,2)
        except:
            # situation where "One person find this review helpful"
            helpful_num, total_num = ("1","1")
    else:
        helpful_num, total_num = ("0","0")

    review_dict = {
                    'userID':userID,
                    'star_rate':star_rate,
                    'device':device,
                    'date':date,
                    'head':head,
                    'review_text':review_text,
                    'helpful_num':helpful_num,
                    'total_num':total_num,
                    }
    # print(review_dict)

    with open('allreviews.json','a') as f:
        f.write(json.dumps(review_dict,indent = 4)+'\n')
    time.sleep(1)

# set up
browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get("https://www.microsoft.com/en-us/p/red-dead-redemption-2/bpswgqbw7r3g?cid=msft_web_chart&activetab=pivot%3Areviewstab")
browser.refresh()
# time.sleep(2)
filter_by = browser.find_element_by_id("displayMode")
# start_filter = browser.find_element_by_id("starfilter")
order_by = browser.find_element_by_id("orderby")
# time.sleep(1)
filter_by.click()
# time.sleep(1)
# cli_displayMode_MostRecent // cli_displayMode_All
browser.find_element_by_id('cli_displayMode_All').click()
# time.sleep(2)
order_by.click()
# time.sleep(1)
# cli_orderby_5 ==> most helpful // cli_orderby_1 ==> most recent
browser.find_element_by_id('cli_orderby_5').click()
# time.sleep(2)

review_index = browser.find_element_by_xpath("//div[@class = 'context-pagination']/span").text
page_num = int(re.match('([0-9]*)-',review_index).group(1))//10
while True:
    if page_num >= 0:
        review_list = browser.find_elements_by_xpath("//div[@class='review cli_review']")
        for i,r in enumerate(review_list):
            try:
                get_info(r)
                print(i+1)
            except:
                pass
        next_page()
        time.sleep(1)
        review_index = browser.find_element_by_xpath("//div[@class = 'context-pagination']/span")
        print(review_index.text)
        page_num = int(re.match('([0-9]*)-',review_index.text).group(1))//10

    elif page_num == 2182:
        break
    else:
        next_page()
        time.sleep(1)
        review_index = browser.find_element_by_xpath("//div[@class = 'context-pagination']/span")
        print(review_index.text)
        page_num = int(re.match('([0-9]*)-',review_index.text).group(1))//10


        # some time the page won't load
        # this is to counter that situation
