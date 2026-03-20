
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
