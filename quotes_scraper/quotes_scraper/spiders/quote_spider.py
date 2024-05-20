import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

from ..items import QuoteItem

class NotAnIntegerError(Exception):
    """Exception raised for errors in the input if it's not an integer."""
    def __init__(self, message="Input is not an integer"):
        self.message = message
        super().__init__(self.message)


class QuoteSpider(CrawlSpider):
    name = "quotespider"
    start_urls = [
        'https://www.goodreads.com/quotes',
    ]

    rules = (
        # Allow only link those include quotes and crawl
        Rule(LinkExtractor(allow=(r'/quotes/.*',)), callback='parse_quotes', follow=True),
        # Rule(LinkExtractor(allow=(r'/quotes/tag/knowledge',)), callback='parse_quotes', follow=True),
    )

    follow_limit = 10
    followed_count = 0

    def __init__(self, *args, **kwargs):
        super(QuoteSpider, self).__init__(*args, **kwargs)
        try:
            self.follow_limit = int(self.follow_limit)
        except (ValueError, TypeError):
            raise NotAnIntegerError(f"Input '{self.follow_limit}' is not an integer")

    def parse_quotes(self, response):
        # raise CloseSpider(reason=f"Reached {self.follow_limit} iterations.")
        self.followed_count += 1
        for quote in response.css('div.quoteDetails'):
            item_quote = quote.css('div.quoteText::text').get()
            item_author = quote.css('span.authorOrTitle::text').get()
            item_tags = quote.css('div.greyText.smallText.left > a::text').getall()
            quote_item = QuoteItem(quote=item_quote, author=item_author, tags=item_tags)
            yield quote_item
        if self.followed_count >= self.follow_limit:
            self.log(f"Followed {self.followed_count} iterations. Closing spider.")
            raise CloseSpider(reason=f"Reached {self.follow_limit} iterations.")

        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_quotes)
