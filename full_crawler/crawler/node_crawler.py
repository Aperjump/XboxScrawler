import re
import os
import sys
import time
import json
import random
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from multiprocessing import Queue

file_path = os.path.abspath(__file__)
poolnum = 5
webdrivers = [webdriver.Chrome() for i in range(poolnum)]
def webcrawl(index, url, que):
    browser = webdrivers[index]


    browser.get(url)
    time.sleep(1)
    ads = browser.find_element_by_xpath("//div[@class='sfw-dialog']")
    tab_index = ads.get_attribute("tabindex")
    if tab_index == '0':
        ads_close = ads.find_element_by_xpath(".//div[@class='c-glyph glyph-cancel']")
        ads_close.click()
    try:
        review_page = browser.find_element_by_xpath("//a[@id='pivot-tab-ReviewsTab']")
        review_page.click()
    except NoSuchElementException as e:
        que.put(index)
        return
    time.sleep(2)
    item_name = browser.find_element_by_xpath("//h1[@id='DynamicHeading_productTitle']").text
    print(str(index) + " receive game " + item_name)
    storage_path = "../data/" + item_name + ".json"
    category = browser.find_element_by_xpath("//div[@aria-label='Category']/a").text
    for num in range(3):
        try:
            filter_by = browser.find_element_by_xpath("//div[@class='c-select-menu  cli_menu_displayMode f-persist']")
            filter_by.click()
            time.sleep(2)
            all_review = filter_by.find_element_by_xpath(".//a[@data-display-caption='All reviews']")
            all_review.click()
            break
        except Exception as e:
            if num < 2:
                time.sleep(3)
                browser.refresh()
                ads = browser.find_element_by_xpath("//div[@class='sfw-dialog']")
                tab_index = ads.get_attribute("tabindex")
                if tab_index == '0':
                    ads_close = ads.find_element_by_xpath(".//div[@class='c-glyph glyph-cancel']")
                    ads_close.click()
                pass
            else:
                print("chrome index " + str(index) + " cannot process " + url)
                print(e)
                que.put(index)
                return
    time.sleep(2)
    #order_by = browser.find_element_by_id("orderby")
    #order_by.click()
    review_index = browser.find_element_by_xpath("//div[@class = 'context-pagination']/span").text
    tot_num = review_index.split()[-2].split(",")
    tmp_str = ""
    for i in tot_num:
        tmp_str += i
    tot_num = int(tmp_str)
    tot_counter = 0
    for _ in range(3):
        review_list = browser.find_elements_by_xpath("//div[@class='review cli_review']")
    for i in range(len(review_list)):
        try:
            get_info(browser, review_list[i], storage_path, item_name, category)
        except:
            print("crawl error")
        tot_counter += 1
    print("chrome index " + str(index) + " %.2f" % (tot_counter / tot_num))

    while next_page(browser):
        time.sleep(3)
        review_index = browser.find_element_by_xpath("//div[@class = 'context-pagination']/span").text
        # print("index " + str(index) + " " + review_index)
        for _ in range(3):
            review_list = browser.find_elements_by_xpath("//div[@class='review cli_review']")
        for i in range(len(review_list)):
            #time.sleep(0.2)
            try:
                get_info(browser, review_list[i], storage_path, item_name, category)
            except Exception as e:
                print("crawl error")
            tot_counter += 1
        print("chrome index " + str(index) + " %.2f" % (tot_counter / tot_num))
    que.put(index)
    return


def get_info(browser, r, storage_path, game_name, category):
    ads = browser.find_element_by_xpath("//div[@class='sfw-dialog']")
    tab_index = ads.get_attribute("tabindex")
    if tab_index == '0':
        ads_close = ads.find_element_by_xpath(".//div[@class='c-glyph glyph-cancel']")
        ads_close.click()
    right_box = r.find_element_by_xpath(".//div[@data-grid = 'col-3']")

    star_rate = right_box.find_element_by_xpath(".//div[@class = 'c-rating f-user-rated f-individual']").get_attribute('data-value')
    try:
        device = r.find_element_by_xpath(".//p[@class='c-meta-text']").text
    except:
        device = 'unknown'
    comment_meta = right_box.find_elements_by_xpath(".//p[@class = 'c-paragraph-3']")
    date = comment_meta[0].text
    userID = comment_meta[1].text
    left_box = r.find_element_by_xpath(".//div[@data-grid = 'col-9']/div")
    head = left_box.find_element_by_tag_name('h5').text

    # see if it has the "more" button to click and expand
    # button = review_area.find_element_by_tag_name("button")
    # if button.get_attribute('style') == 'display: none;':
    #     review_text = review_area.find_element_by_tag_name('p').text
    # else:
    #     button.click()
    #     time.sleep(0.5)
    #     dialog_box = browser.find_element_by_id('review-comment-dialog')
    #     review_text = dialog_box.find_element_by_xpath(".//div[@role = 'dialog']//p[@class = 'c-paragraph']").text
    #     # to counter situation where element is not visible
    #     for _ in range(3):
    #         try:
    #             close_dialog_button = dialog_box.find_element_by_tag_name('button')
    #             close_dialog_button.click()
    #             break
    #         except:
    #             pass

    review_area = left_box.find_element_by_xpath(".//div[@class='c-content-toggle cli_reviews_content_toggle']")
    review_text = review_area.find_element_by_xpath(".//p").text
    buttom_box = r.find_element_by_xpath(".//div[@data-grid = 'col-12']")
    helpfulness = buttom_box.find_element_by_tag_name('p').text
    if helpfulness != "":
        try:
            helpful_num, total_num = re.search('([0-9,]*) out of ([0-9,]*)', helpfulness).group(1, 2)
        except:
            # situation where "One person find this review helpful"
            helpful_num, total_num = ("1", "1")
    else:
        helpful_num, total_num = ("0", "0")
    if len(review_text) == 0:
        return
    review_dict = {
                    'userID':userID,
                    'star_rate':star_rate,
                    'device':device,
                    'date':date,
                    'head':head,
                    'review_text':review_text,
                    'helpful_num':helpful_num,
                    'total_num':total_num,
                    'game': game_name,
                    'category': category
                    }
    #print(review_dict)
    with open(storage_path,'a') as f:
        f.write(json.dumps(review_dict,indent = 4)+'\n')


def next_page(browser):
    for _ in range(3):
        try:
            next_page_button = browser.find_element_by_xpath("//div[@class = 'context-pagination']").find_elements_by_tag_name("li")[1]
            next_page_button.click()
            return True
        except:
            pass
    return False

if __name__ == "__main__":
    url = "https://www.microsoft.com/en-us/p/the-witcher-3-wild-hunt/br765873cqjd?activetab=pivot:overviewtab"
    que = Queue()
    webcrawl(0, url, que)
    for i in webdrivers:
        i.close()