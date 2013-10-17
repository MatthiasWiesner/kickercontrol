from datetime import timedelta

DB_URI = 'sqlite:///users.db'
DEBUG = True
SECRET_KEY = 'foobarbaz'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
REMEMBER_COOKIE_DURATION = timedelta(days=30)