import argparse
import src.defaults as defaults

def msg(name=None):
    return "cmdInterface [-h] [-b] [-p <argument>]"
    
parser = argparse.ArgumentParser(description='Sample argparse', usage=msg(), formatter_class= lambda prog: argparse.MetavarTypeHelpFormatter(
    prog, max_help_position=100, width=85
))

parser.add_argument('-b', '--coin', dest='coin', help='the type of crypto currency you want to check for', nargs='?', const=defaults.COIN, default=defaults.COIN, type=str)
parser.add_argument('-c', '--currency', help='the type of currency you want the price to be in', nargs='?', const=defaults.CURRENCY, default=defaults.CURRENCY, type=str)
parser.add_argument('-i', '--interval', help='subscribe to updates on the crypto currency in this interval', nargs='?', const=0, default=defaults.NOTIFY_CONSTANT, type=float)
parser.add_argument('-l', '--limit', help='notify when the value of the crypto currency goes below this limit', nargs='?', const=None, default=defaults.LIMIT, type=float)
parser.add_argument('-s', '--sms', help='specify a mobile number to get notified', nargs='?', const=None, default=defaults.SMS, type=int)
parser.add_argument('-e', '--email', help='specify an email address to get notified', nargs='?', const=None, default=defaults.EMAIL, type=str)
parser.add_argument('-t', '--twitter', help='specify your twitter username to get notified', nargs='?', const=None, default=defaults.TWITTER, type=str)

args = parser.parse_args()
print(args)

def getOpt():
    obj = {
        'coin': args.coin,
        'currency': args.currency,
        'interval': args.interval,
        'limit': args.limit,
        'twitter': args.twitter,
        'email': args.email,
        'sms': args.sms
    }
    return obj