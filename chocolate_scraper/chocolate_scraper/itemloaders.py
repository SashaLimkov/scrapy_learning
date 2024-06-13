from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class ChocolateProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    url_in =  MapCompose(lambda x : "https://www.chocolate.co.uk" + x)