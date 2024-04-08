# Logic for starting the crawler
# service.py
import os
import sys

# Configuring Environment Variables
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'AdaptiveArtemisNewsRecommendation.settings'

import django

django.setup()
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapyProject.spiders.my_spider import SmithsonianMagRSSSpider



def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(SmithsonianMagRSSSpider)
    process.start()       # Blocking until the crawl is complete


