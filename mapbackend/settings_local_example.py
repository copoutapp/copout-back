"""
local settings example
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<YOUR SECRET KEY HERE>'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '<YOUR DB NAME HERE>',
        'USER': '<YOUR USERNAME HERE>',
        'PASSWORD': '<YOUR PASSWORD HERE>',
        'HOST': '<YOUR DB HOST HERE>',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = [
    'www.copout.app',
    'localhost',
    '127.0.0.1',
]