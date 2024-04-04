
# Replace the DATABASES section of your settings.py with this
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'EL_Hajj',
    'USER': 'EL_Hajj_owner',
    'PASSWORD': 'JKhUktN7QlZ3',
    'HOST':'ep-summer-term-a292jq9j.eu-central-1.aws.neon.tech',
    'PORT': '5432',
    'OPTIONS': {
      'sslmode': 'require',
    },
    'DISABLE_SERVER_SIDE_CURSORS': True,
  }
}