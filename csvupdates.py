import os
import csv
import random
import time

fieldnames = ['Date', 'Price']

if not os.path.isfile('data.csv'):
    with open('data.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()

def insert_data(price, price_date,):
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        info = {
            'Date': price_date,
            'Price': price,
        }
        csv_writer.writerow(info)
        # print(price_date, price)