import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sptxtl.settings')

application = get_wsgi_application()

<<<<<<< HEAD
app = application
=======
app = application
>>>>>>> bf28f181bbe64b7d315638678f6616aa969b1ecc
