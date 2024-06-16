import scrapy
from quotes_scraper.itemloader import QuoteJSLoader
from quotes_scraper.items import QuotesJSItem
from scrapy_playwright.page import PageMethod

class QuotesJsSpider(scrapy.Spider):
    name = "quotes_js"

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", "div.quote")
            ],
            errback = self.errback,

        ))
        
        
    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()


        for quote in response.css("div.quote"):
            quote_item = QuoteJSLoader(item=QuotesJSItem(), selector=quote)
            quote_item.add_css("quote",  "span.text ::text")
            quote_item.add_css("author", "small.author ::text")
            tags = [tag.css("::text").get() for tag in quote.css("div.tags > a")]
            quote_item.add_value("tags", tags)
            yield quote_item.load_item()
        
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page_url = "https://quotes.toscrape.com" + next_page
            
            yield scrapy.Request(next_page_url, meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.quote")
                ],
                errback = self.errback,

        ))

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()