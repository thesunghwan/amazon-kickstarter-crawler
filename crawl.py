import scrapy

class AmazonKickstarter(scrapy.Spider):
    name = "amazon-kickstarter"
    start_urls = [
        'https://www.amazon.com/b?node=13514636011',
    ]

    def parse(self, response):
        for card in response.css("li.s-result-item"):
            yield {
                'title': card.css("h2.a-size-base::text").extract_first(),
                'price': card.css("span.a-size-base.a-color-price.s-price::text").extract_first()
            }

        next_page = response.css('div#pagn a#pagnNextLink::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
