# WSGI configuration file for PythonAnywhere
# Cole este conteúdo no WSGI file do PythonAnywhere

import os
import sys

# Add your project directory to sys.path
path = '/home/yourusername/Quilombo/quilombo_site'  # MUDE 'yourusername' pelo seu username
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quilombo_site.settings')

# Activate virtual environment  
activate_this = '/home/yourusername/Quilombo/quilombo_site/venv/bin/activate_this.py'  # MUDE 'yourusername'
try:
    exec(open(activate_this).read(), dict(__file__=activate_this))
except FileNotFoundError:
    pass

# Import Django WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()