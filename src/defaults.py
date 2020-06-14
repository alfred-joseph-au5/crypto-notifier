from dotenv import load_dotenv
load_dotenv()
import os

API = "https://rest.coinapi.io/v1/exchangerate"
API_KEYS = os.getenv('API_KEYS').split(", ")
API_KEY_HEADER = 'X-CoinAPI-Key'
API_HEADER = {
    'Accept': 'application/json',
    'Accept-Encoding': 'deflate, gzip',
}
API_CURSOR = 0
API_HIT_COUNTER = 0

GMAIL_ID = os.getenv('I_MAIL')
GMAIL_PASSWORD = os.getenv('P_MAIL')

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

VONAGE_KEY = os.getenv('VONAGE_KEY')
VONAGE_SECRET = os.getenv('VONAGE_SECRET')

NOTIFY_CONSTANT = 0.5
CURRENCY = 'USD'
COIN = 'BTC - Bitcoin'
LIMIT = False
NOTIFY = False
TWITTER = False
EMAIL = False
SMS = False