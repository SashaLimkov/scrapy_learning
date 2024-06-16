from typing import Iterable
import scrapy
from quotes_scraper.itemloader import QuoteLoader
from quotes_scraper.items import QuotesItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com"]

    # def start_requests(self):
    #     url = "https://quotes.toscrape.com/"
    #     yield scrapy.Request(url, meta={"playwright":True})
        
        
    def parse(self, response):
        print(response.css("div.quote"))
        for quote in response.css("div.quote"):
            quote_item = QuoteLoader(item=QuotesItem(), selector=quote)
            quote_item.add_css("quote",  "span.text ::text")
            quote_item.add_css("author", "small.author ::text")
            quote_item.add_css("author_link", "span > a::attr(href)")
            tags = {}
            for tag in quote.css("div.tags > a"):
                name = tag.css("::text").get()
                tags[name] = tag.css("::attr(href)").get() 
            quote_item.add_value("tags", tags)
            yield quote_item.load_item()
        
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page_url = "https://quotes.toscrape.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)