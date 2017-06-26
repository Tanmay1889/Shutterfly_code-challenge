"""
This script used to create dummy event data to validate main program.
In order to run this program, Faker needs to be installed as: "pip install faker"
"""

import random
import string
from datetime import datetime
from faker import Faker


def random_num(n):
    return ''.join(random.choice('96f55c7d8f42') for _ in xrange(n))

def string_date(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")

def dummy_data(num_customers, path):
    instance_fake = Faker()
    first_iter = True

    with open(path, 'w') as input_file:

        for _ in xrange(num_customers):
            cust_id = random_num(12)
            event_date = instance_fake.date_time_this_decade()
            customer_entity = { 'type': 'CUSTOMER', 'verb': 'NEW', 'key': cust_id, 'last_name': instance_fake.last_name(), 'event_time': string_date(event_date), 'adr_city': instance_fake.city(), 'adr_state': instance_fake.state() }
            site_visit = { 'type':'SITE_VISIT', 'verb': 'NEW', 'key': random_num(12),'event_time': string_date(event_date), 'customer_id': cust_id, 'tags':[{random_num(12): random_num(12)}] }
            image = { 'type': 'IMAGE', 'verb': 'UPLOAD', 'key': random_num(12), 'event_time': string_date(event_date), 'customer_id': cust_id, 'camera_make':instance_fake.company(), 'camera_model':instance_fake.ean8() }
            order = { 'type': 'ORDER', 'verb': 'NEW', 'key': random_num(12), 'event_time': string_date(event_date), 'customer_id': cust_id, 'total_amount': "{:.2f} USD".format(random.uniform(4, 500)) }
            # Write customer entry
            if first_iter:
                input_file.write('[' + str(customer_entity))
                input_file.write(',\n' + str(site_visit))
                input_file.write(',\n' + str(image))
                input_file.write(',\n' + str(order))
                first_iter = False
            else:
                input_file.write(',\n' + str(customer_entity))
                input_file.write(',\n' + str(site_visit))
                input_file.write(',\n' + str(image))
                input_file.write(',\n' + str(order))


        input_file.write(']')
        print "\nCreated ({}) customer entries in file: {}".format(num_customers, path)


if __name__ == '__main__':
    new_customers = 10
    fpath = "input.txt"
    dummy_data(new_customers, fpath)