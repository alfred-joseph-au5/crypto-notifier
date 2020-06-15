# import os
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import nexmo
import tweepy

import config as config
import defaults as defaults

fetch_url = ""
fetch_headers = {}

# Function to set up the connection for: CoinAPI
# https://rest.coinapi.io/v1/exchangerate/<coin_type>/<currency>
def setup_coin_api():
    global fetch_url
    global fetch_headers
    # making the url with the selected options
    # defaults.API + '/' + config.coin + '/' + config.currency
    fetch_url = '/'.join([defaults.API, config.coin, config.currency])
    # adding request headers
    fetch_headers = defaults.API_HEADER
    fetch_headers[defaults.API_KEY_HEADER] = defaults.API_KEYS[1]

# Funtion to setup the connection for: Nomics API
# https://api.nomics.com/v1/currencies/ticker?interval=1d&key=<KEY>&ids=<coins>&convert=<currency>
def setup_nomics_api():
    global fetch_url
    fetch_url = ''.join([
        defaults.NOMICS_API, defaults.NOMICS_API_KEYS[1], 
        '&ids=', config.coin, '&convert=', config.currency
    ])

# Function to fetch data from CoinAPI
def fetch_new_price_coin_api():
    req = requests.get(fetch_url, headers = fetch_headers)
    response = req.json()
    return response

# Function to fetch data from NomicsAPI
def fetch_new_price_nomics_api():
    req = requests.get(fetch_url)
    response = req.json()
    return response

# Function to send email to anyone using your Gmail account
def send_email():
    try:
        # Creates SMTP session
        session = smtplib.SMTP('smtp.gmail.com', 587)
        # Start TLS for security
        session.starttls() 
        # Authentication
        session.login(defaults.GMAIL_ID, defaults.GMAIL_PASSWORD)
        # Create a message container - multipart/alternative
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Crypto Update!'
        msg['From'] = 'Crypto Notifier'
        msg['To'] =  config.email
        # Body of the email
        html = ' '.join([
                config.msg, 
                '<br>𝑪𝒓𝒚𝒑𝒕𝒐 𝑵𝒐𝒕𝒊𝒇𝒊𝒆𝒓 by 𝐴𝑙𝑓𝑟𝑒𝑑 𝐽𝑜𝑠𝑒𝑝𝘩'
            ])
        # Record and attach the MIME type
        msg.attach(MIMEText(html, 'html'))
        # Sending the mail
        session.sendmail(
            "Crypto Notifier", 
            config.email, 
            msg.as_string()
        )
        # Terminating the session
        session.quit()
        return True
    except:
        return False

# Function to notify the price of the coin on twitter DM
def twitter_dm():
    try:
        # Authorization of consumer key and consumer secret 
        auth = tweepy.OAuthHandler(
            defaults.TWITTER_CONSUMER_KEY, 
            defaults.TWITTER_CONSUMER_SECRET
        ) 
        # Set access to user's access key and access secret  
        auth.set_access_token(
            defaults.TWITTER_ACCESS_TOKEN, 
            defaults.TWITTER_ACCESS_TOKEN_SECRET
        ) 
        # Connect with the API
        api = tweepy.API(auth) 
        # Getting ID of the recipient
        recipient_id = api.get_user(screen_name = config.twitter)
        recipient_id = recipient_id.id    
        # Text to be sent 
        text = ''.join([
            config.msg, '\n𝑪𝒓𝒚𝒑𝒕𝒐 𝑵𝒐𝒕𝒊𝒇𝒊𝒆𝒓 by 𝐴𝑙𝑓𝑟𝑒𝑑 𝐽𝑜𝑠𝑒𝑝𝘩\n'
        ])
        # Sending the direct message 
        api.send_direct_message(recipient_id, text) 
        return True
    except:
        return False

# Function to notify via SMS using Nexmo / Vonage
def send_sms():
    try:
        # Setup up the nexmo client
        client = nexmo.Client(
            key = defaults.VONAGE_KEY, 
            secret = defaults.VONAGE_SECRET
        )
        # Send a message
        client.send_message({
            'from': 'Vonage APIs',
            'to': defaults.VONAGE_NUMBER,
            # Intented formatting after \n
            'text': ''.join([
                config.msg, 
                '\n\nCrypto Notifier by Alfred Joseph. \n \n'
            ])
        })
        return True
    except:
        return False
