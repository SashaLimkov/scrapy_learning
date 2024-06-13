import scrapy
from chocolate_scraper.items import ChocolateProduct
from chocolate_scraper.itemloaders import ChocolateProductLoader

class ChocolateSpiderSpider(scrapy.Spider):
    name = "chocolate_spider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css("product-item")
        for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css("name", "div.product-item-meta a::text")
            chocolate.add_css("url", "div.product-item-meta a::attr(href)")
            yield chocolate.load_item()
            
        next_page = response.css('[rel="next"] ::attr(href)').get()
        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page
            yield response.follow(next_page_url, callback=self.parse)


