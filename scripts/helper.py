from datetime import datetime
from json import loads

def process_time(time):
    time = time.strftime('%Y-%m-%dT%H:%M:%S')
    return time

def convert_dict_to_string(message):
    "May not use this function as dictionary seems to be working fine."
    msg_str = ''
    for key, value in message.items():
        if value:
            msg_str += value + "cs631separator" #cs631separator because , or ; may be in the tweet itself.
        else:
            msg_str += "NAcs631separator"

    return msg_str


def get_products_to_track(return_dict = 0):

    # load and read json file
    with open("products_to_track.json") as f:
        data = loads(f.read())

    # get products list
    products_to_track = []
    for company in data:
        products_to_track += data[company]

    if return_dict == 1:
        return products_to_track, data

    return products_to_track

def get_associated_company_and_product(tweet):

    tweet = tweet.lower()

    # load json data
    products_to_track, data = get_products_to_track(return_dict=1)

    companies = [company for company in data]
    company_found = 0
    associated_company = ""
    associated_product = ""

    for product in products_to_track:
        if product.lower() in tweet:
            for company in companies:
                if product in data[company]:
                    associated_company = company
                    associated_product = product
                    company_found += 1

        # keeping it simple for now. also since search products are more explicit now,
        # the exact substring match may suffice.

        # else:
        #     product_tokens = product.split(" ")
        #     if len(product_tokens) == 2:
        #             if product_tokens[0] in tweet and product_tokens[1] in tweet:
        #                 for company in companies:
        #                     company_products = ' '.join(data[company])
        #                     if product_tokens[0] in company_products and product_tokens[1] in company_products:
        #                         associated_company = company
        #                         company_found += 1


        #     if len(product_tokens) == 3:
        #             if product_tokens[0] in tweet and product_tokens[1] in tweet and product_tokens[2] in tweet:
        #                 for company in companies:
        #                     company_products = ' '.join(data[company])
        #                     if product_tokens[0] in company_products and product_tokens[1] in company_products and product_tokens[2] in company_products:
        #                         associated_company = company
        #                         company_found += 1

    # the code does not differentiate between multiple companies and multiple products
    # for now :)
    if company_found > 1:
        return ("mix", "mix")
    elif company_found == 0:
        return ("none", "none")
    elif company_found == 1:
        return associated_company, associated_product

#print(get_associated_company_and_product("Samsung Galaxy Buds Pro see 1-day discount down to $165 (Sav"))
