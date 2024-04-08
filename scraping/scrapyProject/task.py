# Using Asynchronous Task Queues, Timed Task Scripts
from celery import shared_task
from scraping.scrapyProject.scrapyProject.spiders import my_spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
from scrapy.utils.log import configure_logging

@shared_task
def scrape():
    # process = CrawlerProcess(get_project_settings())
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    logger = logging.getLogger(__name__)
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(my_spider.SmithsonianMagRSSSpider)
        process.start()
        logger.info("Scrapy task completed successfully.")
    except Exception as e:
        logger.error(f"Scrapy task failed with exception: {e}")