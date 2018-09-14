import scrapy
import json
from selenium import webdriver

class FortnightCrawler(scrapy.Spider):
    name = 'Fortnight'
    tot_list = []

    def __init__(self):
        # use any browser you wish
        self.browser = webdriver.Chrome()

    def __del__(self):
        self.browser.close()

    def start_requests(self):
        urls = ["https://www.microsoft.com/en-us/p/fortnite-standard-founders-pack/bxwnx8st04js?activetab=pivot:reviewstab"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_function(self, selector):
        id = selector.xpath("@data-review-id").extract_first()
        text = selector.xpath("//div[@class='c-content-toggle "
                          "cli_reviews_content_toggle']/p/text()").extract_first().strip()
        star = selector.xpath("//div[@class='c-rating f-user-rated f-individual']/@data-value").extract_first()
        header =  selector.xpath("//h5[@class='c-heading-6']/@aria-label").extract_first()
        helpful = selector.xpath("//div[@class='reviewFocusContainer']/div/p[@class='c-meta-text']/text()").extract_first()
        tuple_row = {'review_id': id, 'star': star, 'header': header, 'helpful': helpful, 'comment': text}
        return tuple_row

    def parse_page(self, response):
        review_section = response.xpath("//div[@class='srv_reviews']")
        tuple_list = [self.parse_function(iter) for iter
                      in review_section.xpath("//div[@class='review cli_review']")]
        self.tot_list += tuple_list

    def parse(self, response):
        self.browser.get(response.url)
        self.browser.find_element_by_xpath("//a[@id='reviewsPageNextAnchor']").click()
        self.parse_page(response)
        json_str = json.dumps(self.tot_list)
        fileObject = open('testdata.json', 'w')
        fileObject.write(json_str)
        fileObject.close()
