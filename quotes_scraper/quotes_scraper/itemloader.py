from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class QuoteLoader(ItemLoader):
    def tag_linker(tags):
        for name, link in tags.items():
            tags[name] = "https://quotes.toscrape.com" + link
        return tags
    
    
    default_output_processor = TakeFirst()
    author_link_in =  MapCompose(lambda x : "https://quotes.toscrape.com" + x)
    tags_in = MapCompose(tag_linker)
    
