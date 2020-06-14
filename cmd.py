import requests
import time
import interface_cmd as cmd
import src.pinger as pinger
import src.defaults as defaults
import src.config as config
import src.validation as validate
import currency as currency
import coin as coin
# print(cmd.getOpt()['type'])

args = cmd.getOpt()

def setupconfig():
    args = cmd.getOpt()
    config.currency = args['currency']
    config.coin = (args['coin']).split()[0]
    config.limit = args['limit']
    config.notify = args['interval']
    config.twitter = args['twitter']
    config.email = args['email']
    config.sms = args['sms']
    valid = True

    if(not validate.validate_email(config.email)):
        config.email = defaults.EMAIL
        valid = False
        return valid

    if(not validate.validate_mobile(str(config.sms))):
        config.sms = defaults.SMS
        valid = False
        return valid
    return valid

def infinite_hack():
    count = 0
    while(True):
        response = pinger.fetch_new_price()
        if 'error' in response:
            #Show Error Message and stop the service
            print(response['error'])
            stopservice()
            return
        print(response)
        
        newRate = round(response['rate'], 2)
        selectCoin = config.coin.split(' - ', 1)[1]
        config.msg = 'Hey!\nThe Value of ' + selectCoin + ' is now ' + config.currency.strip() + ' ' + str(newRate)

        if(config.notify is not False):
            count += 15000
            if(config.limit is not False):
                if(newRate < config.limit):
                    pinger.send_notification()
                    count=0
            notifyAt = round(60000 * float(config.notify))
            if(count == notifyAt):
                pinger.send_notification()
                count = 0
        time.sleep(15000)
        # timetraveler = root.after(15000, infinite_hack) #15s

def startservice():
    if(setupconfig()):
        print('Crpto Notifier Monitoring: ')
        pinger.setup_connection()
        print(config.currency, config.coin, config.limit, config.notify, config.twitter, config.email, config.sms)
        infinite_hack()

def stopservice():
    print('service stopped!')
