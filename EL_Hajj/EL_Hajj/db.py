
# Replace the DATABASES section of your settings.py with this
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'EL_Hajj_db',
    'USER': 'EL_Hajj_db_owner',
    'PASSWORD': 'huta9wRAo5IE',
    'HOST':'ep-soft-forest-a2glylyv-pooler.eu-central-1.aws.neon.tech',
    'PORT': '5432',
    'OPTIONS': {
      'sslmode': 'require',
    },
    'DISABLE_SERVER_SIDE_CURSORS': True,
  }
}