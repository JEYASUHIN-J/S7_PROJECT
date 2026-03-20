import os
import sys
import django
from django.conf import settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Aggregator.settings')
django.setup()

# Get the base directory
BASE_DIR = settings.BASE_DIR

# Add crawler directories to path
crawler_dirs = [
    os.path.join(BASE_DIR),
    os.path.join(BASE_DIR, 'newscrawler'),
    os.path.join(BASE_DIR, 'economycrawler'),
    os.path.join(BASE_DIR, 'sportscrawler'),
    os.path.join(BASE_DIR, 'politicscrawler'),
    os.path.join(BASE_DIR, 'lifestylecrawler'),
    os.path.join(BASE_DIR, 'entertainmentcrawler'),
]

# Add each directory to Python path
for directory in crawler_dirs:
    if directory not in sys.path:
        sys.path.append(directory)
        logger.info(f"Added {directory} to Python path")

# Test imports
from news.models import Headline, SHeadline, ENHeadline, EHeadline
logger.info(f"Initial counts - Technology: {Headline.objects.count()}, Sports: {SHeadline.objects.count()}, Entertainment: {ENHeadline.objects.count()}, Economy: {EHeadline.objects.count()}")

# Try importing spiders
try:
    from newscrawler.spiders.news_spider import NewsSpider, TechSpider
    logger.info("✓ Successfully imported Technology spiders")
except ImportError as e:
    logger.error(f"✗ Failed to import Technology spiders: {e}")

try:
    from sportscrawler.spiders.sports_spider import SportsSpider, HtimesSpider
    logger.info("✓ Successfully imported Sports spiders")
except ImportError as e:
    logger.error(f"✗ Failed to import Sports spiders: {e}")

try:
    from entertainmentcrawler.spiders.entertainment_spider import EntertainmentSpider, EntrtnmentSpider
    logger.info("✓ Successfully imported Entertainment spiders")
except ImportError as e:
    logger.error(f"✗ Failed to import Entertainment spiders: {e}")

# Fix the sys.path issue in Django's views.py
logger.info("\nCreating a path configuration file for the project...")

with open(os.path.join(BASE_DIR, 'crawler_paths.py'), 'w') as f:
    f.write("""
import os
import sys

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add crawler directories to path
crawler_dirs = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'newscrawler'),
    os.path.join(BASE_DIR, 'economycrawler'),
    os.path.join(BASE_DIR, 'sportscrawler'),
    os.path.join(BASE_DIR, 'politicscrawler'),
    os.path.join(BASE_DIR, 'lifestylecrawler'),
    os.path.join(BASE_DIR, 'entertainmentcrawler'),
]

# Add each directory to Python path
for directory in crawler_dirs:
    if directory not in sys.path:
        sys.path.append(directory)
""")

# Update views.py to use the path configuration
views_path = os.path.join(BASE_DIR, 'news', 'views.py')
with open(views_path, 'r') as f:
    content = f.read()

# Check if we need to add the import
if 'import crawler_paths' not in content:
    new_content = content.replace(
        '#for scrapy\nimport os\nimport sys',
        '#for scrapy\nimport os\nimport sys\nimport crawler_paths'
    )
    
    # Replace the sys.path.append lines with a comment
    new_content = new_content.replace(
        """path = django_settings.BASE_DIR
sys.path.append(path + "/newscrawler")
sys.path.append(path + "/economycrawler")
sys.path.append(path + "/sportscrawler")
sys.path.append(path + "/politicscrawler")
sys.path.append(path + "/lifestylecrawler")
sys.path.append(path + "/entertainmentcrawler")""",
        """# Path configuration is now handled by crawler_paths.py
path = django_settings.BASE_DIR"""
    )
    
    with open(views_path, 'w') as f:
        f.write(new_content)
    
    logger.info(f"✓ Updated {views_path} to use the new path configuration")
else:
    logger.info(f"⚠ No changes needed for {views_path}")

logger.info("\nNow restart the Django server and try the scrapers again.\n")
logger.info("Visit these URLs in your browser:")
logger.info("1. http://127.0.0.1:8000/scrape/  (for Technology news)")
logger.info("2. http://127.0.0.1:8000/scrape2/ (for Sports news)")
logger.info("3. http://127.0.0.1:8000/scrape5/ (for Entertainment news)") 