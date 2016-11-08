import scrapy
import time

class AmazonKickstarter(scrapy.Spider):
    name = "amazon-kickstarter"
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
    }
    start_urls = [
        'https://www.amazon.com/b?node=13514636011',
    ]

    def parse(self, response):
        for card in response.css("li.s-result-item"):
            link = card.css(".a-link-normal.a-text-normal::attr('href')").extract_first()
            yield scrapy.Request(link, callback=self.parse_page)


        """next_page = response.css('div#pagn a#pagnNextLink::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)"""

    def parse_page(self, response):
        try:
            product_name = response.css("h1#title span::text").extract_first().strip()
        except:
            try:
                product_name = response.css("#title_feature_div h1::text").extract_first().strip()
            except:
                try:
                    product_name = response.css("h1#aiv-content-title::text").extract_first().strip()
                except:
                    product_name = response.css(".buying .parseasinTitle #btAsinTitle::text").extract_first().strip()

        try:
            brand = response.css("#brand::text").extract_first().strip()
        except:
            try:
                brand = response.css(".author a::text").extract_first().strip()
            except:
                try:
                    brand = response.css(".author span::text").extract_first().strip()
                except:
                    try:
                        brand = response.css("#ProductInfoArtistLink::text").extract_first().strip()
                    except:
                        brand = response.css(".buying span a::text").extract_first().strip()

        yield {
            'product_name': product_name,
            'brand': brand,
            'url': response.url,
        }

        """try:
            avgRating = response.css("div#avgRating a span::text").extract_first().strip().split(" ")[0]
        except:
            #홈페이지엔 존재하는 경우에도 나타날 수 있음.
            avgRating = "N/A"

        try:
            price = response.css("#priceblock_ourpice_row #priceblock_ourpice::text").extract_first()
        except:
            print("aa")"""

        """yield {
            'product_name': product_name,
            'avgRating': avgRating,
            'url': response.url,
            'price': price
        }"""
