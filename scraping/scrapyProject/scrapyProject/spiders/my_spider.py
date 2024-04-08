# Handle data crawling and cleansing (ETL)

import scrapy
from ..items import ArticleItem

# RSS source
class SmithsonianMagRSSSpider(scrapy.Spider):
    name = 'mag_rss'
    allowed_domains = [
        'smithsonianmag.com',
        'newscientist.com'
    ]
    start_urls = [
        'https://www.smithsonianmag.com/rss/latest_articles/',
        'https://www.smithsonianmag.com/rss/air-space-magazine/',
        'https://www.smithsonianmag.com/rss/articles/',
        'https://www.smithsonianmag.com/rss/arts-culture/',
        'https://www.smithsonianmag.com/rss/smithsonian-institution/',
        'https://www.smithsonianmag.com/rss/history/',
        'https://www.smithsonianmag.com/rss/innovation/',
        'https://www.smithsonianmag.com/rss/magazine/',
        'https://www.smithsonianmag.com/rss/newsletters/',
        'https://www.smithsonianmag.com/rss/multimedia/',      # Photos
        'https://www.smithsonianmag.com/rss/science-nature/',  # Science
        'https://www.smithsonianmag.com/rss/second-opinion/',
        'https://www.smithsonianmag.com/rss/travel/',

        'https://www.newscientist.com/feed/home/',
        'https://www.newscientist.com/section/news/feed/',
        'https://www.newscientist.com/section/features/feed/',
        'https://www.newscientist.com/subject/physics/feed/',
        'https://www.newscientist.com/subject/technology/feed/',
        'https://www.newscientist.com/subject/space/feed/',
        'https://www.newscientist.com/subject/life/feed/',
        'https://www.newscientist.com/subject/earth/feed/',
        'https://www.newscientist.com/subject/health/feed/',
        'https://www.newscientist.com/subject/humans/feed/'
    ]

    def parse(self, response):
        # Parsing and getting fields through items
        for item in response.xpath('//channel/item'):
            article_item = ArticleItem(
                title=item.xpath('title/text()').get().strip(),
                link=item.xpath('link/text()').get().strip(),
                description=item.xpath('description/text()').get().strip(),
                pubDate=item.xpath('pubDate/text()').get().strip(),
                image=item.xpath('enclosure/@url').get().strip()
            )

            request = scrapy.Request(                    # Extract Link for each record
                article_item['link'],
                callback=self.parse_article_detail
            )
            request.meta['article_item'] = article_item  # Passing the current entry as meta data
            yield request

    def parse_article_detail(self, response):            # Parsing the details of an article from the response
        article_item = response.meta['article_item']
        article_item['keywords'] = response.css('meta[name="keywords"]::attr(content)').get()
        article_item['robots'] = response.css('meta[name="robots"]::attr(content)').get()
        article_item['author'] = response.css('meta[name="author"]::attr(content)').get()
        article_item['category'] = response.css('meta[name="category"]::attr(content)').get()
        article_item['body'] = response.css('div.article-body').get()                 # getting body
        yield article_item







#
#
# # CSS source
# class SmithsonianMagSpider(scrapy.Spider):
#     name = 'smithsonian_mag'
#     allowed_domains = ['smithsonianmag.com']
#     start_urls = ['https://www.smithsonianmag.com/']
#
#     def parse(self, response):        # Select the URLs of the articles or sections
#         for article in response.css('article'):
#             url = article.css('a::attr(href)').get()
#             yield response.follow(url, self.parse_article)
#
#     def parse_article(self, response):    # Extract data from the article page
#         yield {
#             'title': response.css('h1::text').get(),
#             'author': response.css('.author-name::text').get(),
#             'publication_date': response.css('.published-date::text').get(),
#             'content': " ".join(response.css('.article-content p::text').getall()),
#         }
