import os
import sys
import django
import logging

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Aggregator.settings')
django.setup()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import models and check counts
from news.models import Headline, SHeadline, ENHeadline, EHeadline
logger.info(f"Initial counts - Technology: {Headline.objects.count()}, Sports: {SHeadline.objects.count()}, Entertainment: {ENHeadline.objects.count()}, Economy: {EHeadline.objects.count()}")

# Import Scrapy components
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from crochet import setup

# Initialize the Technology crawler
try:
    from newscrawler.spiders.news_spider import NewsSpider, TechSpider
    from newscrawler import settings as tech_settings
    has_tech_spider = True
    logger.info("Successfully imported Technology spiders")
except ImportError as e:
    logger.error(f"Failed to import Technology spiders: {e}")
    has_tech_spider = False

# Initialize the Sports crawler
try:
    from sportscrawler.spiders.sports_spider import SportsSpider, HtimesSpider
    from sportscrawler import settings as sports_settings
    has_sports_spider = True
    logger.info("Successfully imported Sports spiders")
except ImportError as e:
    logger.error(f"Failed to import Sports spiders: {e}")
    has_sports_spider = False

# Initialize the Entertainment crawler
try:
    from entertainmentcrawler.spiders.entertainment_spider import EntertainmentSpider, EntrtnmentSpider
    from entertainmentcrawler import settings as entertainment_settings
    has_entertainment_spider = True
    logger.info("Successfully imported Entertainment spiders")
except ImportError as e:
    logger.error(f"Failed to import Entertainment spiders: {e}")
    has_entertainment_spider = False

# Setup crochet for running Scrapy in a script
setup()
configure_logging()

def run_technology_crawlers():
    """Run the technology news crawlers"""
    if not has_tech_spider:
        logger.error("Technology spiders not available")
        return

    # Create test record directly
    try:
        test_headline = Headline(title="Test Technology News", image="https://example.com/image.jpg", 
                                url="https://example.com", source="Test")
        test_headline.save()
        logger.info(f"Test technology headline created. Count now: {Headline.objects.count()}")
    except Exception as e:
        logger.error(f"Failed to create test technology headline: {e}")
    
    # Clear existing headlines
    try:
        Headline.objects.all().delete()
        logger.info(f"Technology headlines cleared. Count now: {Headline.objects.count()}")
    except Exception as e:
        logger.error(f"Failed to clear technology headlines: {e}")
    
    # Run the crawler
    logger.info("Starting Technology crawlers...")
    crawler_settings = Settings()
    crawler_settings.setmodule(tech_settings)
    runner = CrawlerRunner(settings=crawler_settings)
    
    logger.info("Running NewsSpider...")
    d1 = runner.crawl(NewsSpider)
    d1.addCallback(lambda _: logger.info("NewsSpider completed"))
    d1.addErrback(lambda failure: logger.error(f"NewsSpider failed: {failure}"))
    
    logger.info("Running TechSpider...")
    d2 = runner.crawl(TechSpider)
    d2.addCallback(lambda _: logger.info("TechSpider completed"))
    d2.addErrback(lambda failure: logger.error(f"TechSpider failed: {failure}"))
    
    d2.addCallback(lambda _: logger.info(f"Final technology headlines count: {Headline.objects.count()}"))

def run_sports_crawlers():
    """Run the sports news crawlers"""
    if not has_sports_spider:
        logger.error("Sports spiders not available")
        return
    
    # Create test record directly
    try:
        test_headline = SHeadline(title="Test Sports News", image="https://example.com/sports.jpg", 
                                url="https://example.com/sports", source="Test")
        test_headline.save()
        logger.info(f"Test sports headline created. Count now: {SHeadline.objects.count()}")
    except Exception as e:
        logger.error(f"Failed to create test sports headline: {e}")
    
    # Clear existing headlines
    try:
        SHeadline.objects.all().delete()
        logger.info(f"Sports headlines cleared. Count now: {SHeadline.objects.count()}")
    except Exception as e:
        logger.error(f"Failed to clear sports headlines: {e}")
        
    # Run the crawler
    logger.info("Starting Sports crawlers...")
    crawler_settings = Settings()
    crawler_settings.setmodule(sports_settings)
    runner = CrawlerRunner(settings=crawler_settings)
    
    logger.info("Running SportsSpider...")
    d1 = runner.crawl(SportsSpider)
    d1.addCallback(lambda _: logger.info("SportsSpider completed"))
    d1.addErrback(lambda failure: logger.error(f"SportsSpider failed: {failure}"))
    
    logger.info("Running HtimesSpider...")
    d2 = runner.crawl(HtimesSpider)
    d2.addCallback(lambda _: logger.info("HtimesSpider completed"))
    d2.addErrback(lambda failure: logger.error(f"HtimesSpider failed: {failure}"))
    
    d2.addCallback(lambda _: logger.info(f"Final sports headlines count: {SHeadline.objects.count()}"))

def run_entertainment_crawlers():
    """Run the entertainment news crawlers"""
    if not has_entertainment_spider:
        logger.error("Entertainment spiders not available")
        return
        
    # Create test record directly
    try:
        test_headline = ENHeadline(title="Test Entertainment News", image="https://example.com/entertainment.jpg", 
                                url="https://example.com/entertainment", source="Test")
        test_headline.save()
        logger.info(f"Test entertainment headline created. Count now: {ENHeadline.objects.count()}")
    except Exception as e:
        logger.error(f"Failed to create test entertainment headline: {e}")
    
    # Clear existing headlines
    try:
        ENHeadline.objects.all().delete()
        logger.info(f"Entertainment headlines cleared. Count now: {ENHeadline.objects.count()}")
    except Exception as e:
        logger.error(f"Failed to clear entertainment headlines: {e}")
    
    # Run the crawler
    logger.info("Starting Entertainment crawlers...")
    crawler_settings = Settings()
    crawler_settings.setmodule(entertainment_settings)
    runner = CrawlerRunner(settings=crawler_settings)
    
    logger.info("Running EntertainmentSpider...")
    d1 = runner.crawl(EntertainmentSpider)
    d1.addCallback(lambda _: logger.info("EntertainmentSpider completed"))
    d1.addErrback(lambda failure: logger.error(f"EntertainmentSpider failed: {failure}"))
    
    logger.info("Running EntrtnmentSpider...")
    d2 = runner.crawl(EntrtnmentSpider)
    d2.addCallback(lambda _: logger.info("EntrtnmentSpider completed"))
    d2.addErrback(lambda failure: logger.error(f"EntrtnmentSpider failed: {failure}"))
    
    d2.addCallback(lambda _: logger.info(f"Final entertainment headlines count: {ENHeadline.objects.count()}"))

if __name__ == '__main__':
    print("Running diagnostic tests for news crawlers...")
    
    # Run the crawlers
    run_technology_crawlers()
    run_sports_crawlers()
    run_entertainment_crawlers()
    
    # Keep the reactor running until all spiders complete
    reactor.run() 