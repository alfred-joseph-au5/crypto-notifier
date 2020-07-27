import sys
import time
import argparse
import requests
from datetime import datetime

import pytz
import tzlocal

import pinger as pinger
import defaults as defaults
import config as config
import validation as validate
import currency as currency
import coin as coin

args = None

# Function to set usuage for the commandline interface
def msg(name = None):
    return ' '.join([
        'cmd [--help]', '[--coin <coin_type>]', 
        '[--currency <currency>]\n', '\t[--interval <time_in_minutes>]',  
        '[--limit <limit>]\n', '\t[--sms <mobile_number>]', 
        '[--email <email_id>]\n', '\t[--twitter <twitter_handle>]'
    ])
    
# Function to setup defaults
def setupconfig():
    config.currency = args['currency']
    config.coin = (args['coin']).split()[0]
    config.limit = args['limit']
    config.notify = args['interval']
    config.twitter = args['twitter']
    config.email = args['email']
    config.sms = args['sms']
    valid = True

    if(config.email is not False):
        if(not validate.validate_email(str(config.email))):
            config.email = defaults.EMAIL
            print(' '.join([
                '\nEmail Error :', 
                'Please enter a valid email ID!'
                ])
            )
            exit()

    if(config.sms is not False):
        if(not validate.validate_mobile(str(config.sms))):
            config.sms = defaults.SMS
            print(' '.join([
                '\nSMS Error :', 
                'Error sending message to the', 
                'number you have provided.',
                'Please check the number and',
                'try again!'
                ])
            )
            exit()
    return valid

def infinite_hack():
    count = 0
    while(True):
        # response = pinger.fetch_new_price_coin_api() #CoinAPI
        response = pinger.fetch_new_price_nomics_api() #Nomics
        if 'error' in response:
            #Show Error Message and stop the service
            # print(response['error'])
            print('\nServer Error!')
            stop_service()
            return
        # print(response)        
        # new_rate = round(response['rate'], 2)  #CoinAPI
        new_rate = round(float(response[0]['price']), 2) #Nomics
        # select_coin = config.coin.split(' - ', 1)[1] #CoinAPI
        select_coin = config.coin #Nomics
        ltz = tzlocal.get_localzone()
        utc_time = datetime.strptime(
            response[0]['price_timestamp'], 
            '%Y-%m-%dT%H:%M:%SZ'
        )
        lt = str(utc_time.replace(tzinfo = pytz.utc).astimezone(ltz))
        lt = lt[0:19]
        config.msg = ' '.join([
            '\nHey!\nThe Value of', select_coin, 'is now', 
            config.currency.strip(), str(new_rate), 
            '\nLast updated on', lt
        ])
        print(config.msg)
        # Check if you have to notify
        if(config.notify is not False):
            count += 15
            # Check if limit is set
            if(config.limit is not False):
                if(new_rate < config.limit):
                    config.msg = ' '.join([
                        '\nHey!\nThe Value of', select_coin, 
                        'has gone below the set limit!!', 
                        '\nThe Value of', select_coin, 'is', 
                        config.currency.strip(), str(new_rate), 
                        'now!\nTake an action ASAP!'
                    ])
                    send_notification()
                    count=0
            # Check for set interval
            # Default interval = 0.5 minutes
            notify_at = round(60 * float(config.notify))
            if(count == notify_at):
                send_notification()
                count = 0
        time.sleep(15)

def send_notification():
    if(config.email is not False):
        if(pinger.send_email() is not True):
            print(
                '\n\nEmail Error:', 
                'Please enter a valid email ID!'
            )
            exit()

    if(config.twitter is not False):
        if(pinger.twitter_dm() is not True):
            print(
                ' '.join([
                    '\n\nTwitter Error:', 
                    'Please check your twitter handle and make sure', 
                    'you have enabled "Receive messages from anyone"', 
                    'setting.\nAccept the message request once', 
                    'you get your first notification.\n'
                ])
            )
            exit()

    if(config.sms is not False):
        if(pinger.send_sms() is not True):
            print(
                ' '.join([
                    '\n\nSMS Error:', 
                    'Error sending message to the number you have', 
                    'provided. Please check the number and try again!\n'
                ])
            )
            exit()
    
def start_service():
    if(setupconfig()):
        print('Crpto Notifier Monitoring: ')
        # pinger.setup_coin_api() #CoinAPI
        pinger.setup_nomics_api() #Nomics
        infinite_hack()

def stop_service():
    print('\n\nExiting...')
    exit()

if __name__ == '__main__':
    # Setup Argparser for command line interface   
    parser = argparse.ArgumentParser(
        description = '\nCrypto Notifier\n', usage = msg(), 
        formatter_class = lambda prog: argparse.MetavarTypeHelpFormatter(
            prog, max_help_position = 100, width = 85
        ))
    # Define new arguments
    parser.add_argument(
        '-b', '--coin', dest ='coin', type=str, 
        help = 'the type of crypto currency you want to check for', 
        nargs = '?', const = defaults.COIN, default = defaults.COIN
    )
    parser.add_argument(
        '-c', '--currency', dest ='currency', type = str, 
        help = 'the type of currency you want the price to be in', 
        nargs = '?', const = defaults.CURRENCY, 
        default = defaults.CURRENCY
    )
    parser.add_argument(
        '-i', '--interval', dest = 'interval', type = float, 
        help = '''subscribe to updates on the crypto currency \
                in this interval''', 
        nargs = '?', const = defaults.NOTIFY_CONSTANT, 
        default = defaults.NOTIFY_CONSTANT
    )
    parser.add_argument(
        '-l', '--limit', dest = 'limit', type = float, 
        help = '''notify when the value of the crypto currency goes \
            below this limit''', 
        default = defaults.LIMIT
    )
    parser.add_argument(
        '-s', '--sms', dest = 'sms', type = int, 
        help = 'specify a mobile number to get notified', 
        default = defaults.SMS
    )
    parser.add_argument(
        '-e', '--email', dest = 'email', type=str, 
        help = 'specify an email address to get notified', 
        default = defaults.EMAIL
    )
    parser.add_argument(
        '-t', '--twitter', dest = 'twitter', type=str, 
        help ='specify your twitter username to get notified', 
        default = defaults.TWITTER
    )
    args = parser.parse_args()
    args = {
        'coin': args.coin,
        'currency': args.currency,
        'interval': args.interval,
        'limit': args.limit,
        'twitter': args.twitter,
        'email': args.email,
        'sms': args.sms
    }
    try:
        start_service()
    #listen for keboard interrupts like ctrl + z or ctrl + c
    except KeyboardInterrupt:
        print('\n\nExiting...')
        exit()