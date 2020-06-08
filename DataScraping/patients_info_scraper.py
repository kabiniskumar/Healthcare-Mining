import scrapy

class MainSpider(scrapy.Spider):

    name = "patients"

    def initialize(self):
        increment_letter = 0
        while increment_letter < 26:
            yield scrapy.Request(url='https://patient.info/forums/index-' + chr(ord('A') + increment_letter), callback=self.start_parsing)
            increment_letter += 1

    def start_parsing(self, response):
        topicURLs = response.xpath("//div[@class='disc-forums disc-a-z']").xpath(".//tr[@class='row-0']//a/@href")
        for each in topicURLs:
            yield scrapy.Request(url=response.urljoin(each.get()), callback=self.processThreads)

    def processThreads(self, response):
        threads = response.xpath("//li[@class='disc-smr cardb']")
        threads = threads[:]
        for threadTitle in threads:
            yield scrapy.Request(url=response.urljoin(threadTitle.xpath(".//h3[@class='post__title']//a/@href").get()), callback=self.processThread)

    def processThread(self, response):
        threadBody = response.xpath("//div[@class='post__content']/p/text()")
        body = ''
        for each in threadBody:
            body += each.get() + ' '
        record = {
            'condition': response.xpath('.//ol[@class="breadcrumbs"]//li[3]//span/text()').extract_first().strip(),
            'postLink': response.threadURL,
            'postHeading': response.xpath("//h1[@class='u-h1 post__title']/text()").get(),
            'postContent': body
        }
        yield record
