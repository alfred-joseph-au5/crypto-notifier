import os
import requests
from dotenv import load_dotenv
load_dotenv()
import smtplib
import nexmo
import tweepy
import src.config as config
import src.defaults as defaults

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fetchUrl = ""
fetchHeaders = {}

def setup_connection():
    global fetchUrl
    global fetchHeaders
    fetchUrl = defaults.API + '/' + config.coin + '/' + config.currency
    fetchHeaders = defaults.API_HEADER
    fetchHeaders[defaults.API_KEY_HEADER] = defaults.API_KEYS[0]
    # print(fetchUrl, 'setup')

def fetch_new_price():
    req = requests.get(fetchUrl, headers= fetchHeaders)
    response = req.json()
    # print(response)
    return response

def send_notification():
    if(config.email is not False):
        send_email()
    if(config.twitter is not False):
        twitter_dm()
    if(config.sms is not False):
        send_sms()

def send_email():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls() 
    s.login(defaults.GMAIL_ID, defaults.GMAIL_PASSWORD)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Crypto Update!'
    msg['From'] = 'Crypto Notifier'
    msg['To'] =  config.email
    
    html = config.msg + """\
        <br>
        𝑪𝒓𝒚𝒑𝒕𝒐 𝑵𝒐𝒕𝒊𝒇𝒊𝒆𝒓 by 𝐴𝑙𝑓𝑟𝑒𝑑 𝐽𝑜𝑠𝑒𝑝𝘩
    """
    msg.attach(MIMEText(html, 'html'))

    # message = """From: Crypto Notifier\nTo: """ + config.email + """\nSubject: Crypto Update!\n""" + config.msg + '\n<b>Cryto Notifier</b> by <b>Alfred Joseph</b>\n'
    s.sendmail("Crypto Notifier", config.email , msg.as_string())
    s.quit()

def twitter_dm():
    # authorization of consumer key and consumer secret 
    auth = tweepy.OAuthHandler(defaults.TWITTER_CONSUMER_KEY, defaults.TWITTER_CONSUMER_SECRET) 
    
    # set access to user's access key and access secret  
    auth.set_access_token(defaults.TWITTER_ACCESS_TOKEN, defaults.TWITTER_ACCESS_TOKEN_SECRET) 

    # calling the api
    api = tweepy.API(auth) 
    
    # getting ID of the recipient 
    recipient_id = api.get_user(screen_name = 'aj8123')
    recipient_id = recipient_id.id
    
    # text to be sent 
    text = config.msg + '\n𝑪𝒓𝒚𝒑𝒕𝒐 𝑵𝒐𝒕𝒊𝒇𝒊𝒆𝒓 by 𝐴𝑙𝑓𝑟𝑒𝑑 𝐽𝑜𝑠𝑒𝑝𝘩\n'
    
    # sending the direct message 
    # direct_message = 
    api.send_direct_message(recipient_id, text) 
    
    # printing the text of the sent direct message 
    # print(direct_message.message_create['message_data']['text'])

    # # authentication of consumer key and secret 
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
    # # authentication of access token and secret 
    # auth.set_access_token(access_token, access_token_secret) 
    # api = tweepy.API(auth) 
    
    # # update the status 
    # api.update_status(status ="Hello Everyone !")

def send_sms():
    # client = nexmo.Client(key='31098d08', secret='S51NWsHqNybu0jsk') # Crypto

    client = nexmo.Client(key = defaults.VONAGE_KEY, secret = defaults.VONAGE_SECRET) # Test

    client.send_message({
        'from': 'Vonage APIs',
        'to': '919535949385',
        'text': config.msg + '\n\nCrypto Notifier by Alfred Joseph. \n \n',
    })

