import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.newsagent.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()