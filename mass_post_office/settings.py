from django.conf import settings

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'some secret key')
EMAIL_TEMPLATES_SHOULD_BE_OVERRIDED = getattr(settings, 
	'EMAIL_TEMPLATES_SHOULD_BE_OVERRIDED', [])