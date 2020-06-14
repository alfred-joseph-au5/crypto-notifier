# Crypto Notifier

A Python program that sends realtime notifications based on the Crypto currency selected.

## Requirements

You need Python 3.x or later to run mypy. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, Mint and Debian you can install Python 3 like this:

    $ sudo apt-get install python3 python3-pip

For other Linux flavors, macOS and Windows, packages are available at https://www.python.org/getit/

## Setup

After installing Python, make sure you have pip installed. If not go [here](https://pip.pypa.io/en/stable/installing/).

You will need to have these packages installed (if not please follow the instructions):
* tkinter (only for GUI) - https://tkdocs.com/tutorial/install.html

* requests

    ```python
    pip install requests
    ```
    
* nexmo

    ```pyhton
    pip install nexmo
    ```
    
* tweepy
    
    ```python
    pip install tweepy
    ```

## Usage

In the root directory there is a gui version as well as a program that runs on the command line interface.
Please select what you want to run.

* GUI - Run this from the root directory of the project in command line / terminal to start the GUI.

    ```
    python gui.py
    ```
    
* CLI - Run this from the root directory of the project to start the command line interface.

    ```
    python cli.py
    ```
### CLI - Optional Arguments

* Usuage:

    ```
    cli [--help] [--coin <coin_type>] [--currency <currency>] [--interval <time_in_minutes>] [--limit <limit>] [--sms <mobile_number>] [--email <email_id>] [--twitter <twitter_handle>]
    ```
    * Optional arguments:
        * `-h, --help`                      show this help message and exit
        * `-b [str], --coin [str]`          the type of crypto currency you want to check for
        * `-c [str], --currency [str]`      the type of currency you want the price to be in
        * `-i [float], --interval [float]`  subscribe to updates on the crypto currency in this interval
        * `-l float, --limit float`         notify when the value of the crypto currency goes below this limit
        * `-s int, --sms int`               specify a mobile number to get notified
        * `-e str, --email str`             specify an email address to get notified
        * `-t str, --twitter str`           specify your twitter username to get notified
