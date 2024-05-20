# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from models.models import Quote, Author, Tag
from models.database import create_table, engine


class QuotesScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['quote'] = adapter.get('quote', '').strip().strip(u'\u201c'u'\u201d')
        adapter['author'] = adapter.get('author', '').strip().lstrip(',').rstrip(',')
        adapter['tags'] = [tag.strip().strip().lstrip(',').rstrip(',') for tag in adapter.get('tags', [])]
        return item


class SaveQuotesPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """

        create_table(engine)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        quote = Quote()
        author = Author()
        author.name = item["author"]
        quote.quote_content = item["quote"]

        # check whether the author exists
        exist_author = session.query(Author).filter_by(name=author.name).first()
        if exist_author is not None:  # the current author exists
            quote.author = exist_author
        else:
            quote.author = author

        if "tags" in item:
            for tag_name in item["tags"]:
                tag = Tag(name=tag_name)
                exist_tag = session.query(Tag).filter_by(name=tag.name).first()
                if exist_tag is not None:  # the current tag exists
                    tag = exist_tag
                quote.tags.append(tag)

        try:
            session.add(quote)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
