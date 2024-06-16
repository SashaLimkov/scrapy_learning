import scrapy
from quotes_scraper.itemloader import QuoteJSLoader
from quotes_scraper.items import QuotesJSItem
from scrapy_playwright.page import PageMethod

class QuotesScrollSpider(scrapy.Spider):
    name = "quotes_scroll"

    def start_requests(self):
        url = "https://quotes.toscrape.com/scroll"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", "div.quote"),
                PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                PageMethod("wait_for_selector", "div.quote:nth-child(11)")
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

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()