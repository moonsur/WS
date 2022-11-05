from ballotspider.spiders import spider_classes as spc
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


url = 'https://ballotpedia.org/Elections_by_state_and_year'
process = CrawlerProcess(get_project_settings())
process.crawl(spc.StateUrls)
process.start()