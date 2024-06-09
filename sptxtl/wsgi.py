import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sptxtl.settings')
application = get_wsgi_application()
<<<<<<< HEAD
app = application
=======
app = application
>>>>>>> 145e1cb58eab4076ed1e47d46821dc66a4026c46
