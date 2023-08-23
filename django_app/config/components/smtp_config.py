import os

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get("EMAIL_HOST", 'smtp.example.com')
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", 'your_username')
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", 'your_password')
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", 'your_email@example.com')