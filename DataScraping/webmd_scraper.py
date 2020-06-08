import scrapy

class WebMDMessageBoardSpider(scrapy.Spider):
    name = "WebMDMessageBoard"

    def start_requests(self):
        start_urls = ("https://messageboards.webmd.com/",)

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        conditions = response.xpath('//*[@id="fragment-2071092687"]/div[1]/div/div/div[3]/div[1]//div[@class="link"]/a/@href').getall()

        for condition in conditions:
            link = response.urljoin(condition)
            yield scrapy.Request(url=link, callback=self.parse_condition)

    def parse_condition(self, response):

        threads = response.xpath('//*[@class="thread-detail"]/h3/a/@href').getall()

        for each in threads:
            post_link = response.urljoin(each)

            yield scrapy.Request(url=post_link, callback=self.parse_thread)

        next_page = response.xpath('//a[@class="next"]/@href').getall()
        print("Next page:", next_page)
        if next_page:
            next_link = response.urljoin(next_page[0])
            yield scrapy.Request(url=next_link, callback=self.parse_condition, dont_filter=True)

    def parse_thread(self, response):
        thread_link = response.url
        thread_heading = response.css("a.internal-link.view-post.unread::text").get()
        thread_details = response.css("ul.content-list.content.margin-bottom.thread-list.webmd-mb-thrd")
        thread_body = " ".join(thread_details.css("div.thread-body::text").getall())
        thread_body = thread_body.strip()
        item = {
            'postLink': thread_link,
            'postHeading': thread_heading,
            'postContent': thread_body
        }
        yield item
