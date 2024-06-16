import scrapy
from quotes_scraper.itemloader import QuoteJSLoader
from quotes_scraper.items import QuotesJSItem
from scrapy_playwright.page import PageMethod

class QuotesScreenShotSpider(scrapy.Spider):
    name = "quotes_screenshot"

    def start_requests(self):
        url = "https://quotes.toscrape.com/scroll"
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod("wait_for_selector", "div.quote"),
            ],
            errback = self.errback,

        ))
        
        
    async def parse(self, response):
        page = response.meta["playwright_page"]
        screenshot = await page.screenshot(path="example.jpg", full_page=True)
        await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()