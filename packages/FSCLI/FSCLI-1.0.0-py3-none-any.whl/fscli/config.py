import os

from dotenv import load_dotenv

load_dotenv()

AT_URL_USERS = os.environ.get('AT_URL_USERS')
AT_KEY = os.environ.get('AT_KEY')
AT_URL_SINGLE_USER = os.environ.get('AT_URL_SINGLE_USER')
