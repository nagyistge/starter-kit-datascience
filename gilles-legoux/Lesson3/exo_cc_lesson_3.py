#!/usr/bin/env python3
"""
Compute the best brand in terms of mean of price decreases on all items
from Cdiscount website.

Here, Dell and Acer are compared.

After running, two files are created:
- data-cdiscount-com-items.csv
- data-cdiscount-com-indicators.csv
"""

# standard library imports
import re
import pprint

# related third party imports
import requests
from bs4 import BeautifulSoup
import pandas

# public global constant
url = 'http://www.cdiscount.com'
csv_items = 'data-cdiscount-com-items.csv'
csv_indicators = 'data-cdiscount-com-indicators.csv'


# public functions
def get_all_items(brands, verbose=False):
    items = []
    for brand in brands:
        url = get_url(brand)
        for page in range(1, get_number_of_pages(url) + 1):
            soup = extract_data_from_page(url, page)
            item = get_items(soup, brand)
            if verbose:
                print(item)
            items.extend(item)
    return items


def persist_items(raw_data):
    global csv_items
    if len(raw_data) == 0:
        return pandas.DataFrame()
    df = pandas.DataFrame(
        raw_data,
        columns=list(raw_data[0].keys())
    )
    df.index.name = 'id'
    df.to_csv(csv_items)
    return df


def compute_indicators_from_csv(csv):
    return compute_indicators(pandas.DataFrame.from_csv(csv))


def compute_indicators(df):
    dff = pandas.DataFrame.copy(df)
    dff = dff.groupby(['brand']).agg(
        {
            'price': sum,
            'old_price': sum
        }
    )
    dff['decrease'] = dff['old_price'] - dff['price']
    dff['decrease_percentage'] = (dff['decrease'] / dff['price']) * 100
    return dff


def persist_indicators(df):
    global csv_indicators
    df.to_csv(csv_indicators)
    return df


# private functions
def get_url(brand):
    global url
    return url + '/search/{}+ordinateur+portable.html'.format(brand)


def extract_data_from_page(url, page):
    result = requests.get(url, params={'page': str(page)})
    if result.status_code == 404:
        sys.stderr.write('ERROR: no data for url {}.\n'.format(result.url))
        exit(1)
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup


def get_number_of_pages(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return int(soup.find('div', class_='pg').find('ul') \
               .find_all('li')[-1].find('span').contents[0])


def get_items(soup, brand):
    url_elt = get_item_block(soup)
    return extract_items(url_elt, brand)


def get_item_block(soup):
    return soup.find('ul', {'id': 'lpBloc'})


def extract_items(ul_elt, brand):
    items = []
    for li_elt in ul_elt.find_all('li', recursive=False):
        if not is_item(li_elt):
            continue
        item = extract_item(li_elt, brand)
        if item:
            items.append(item)
    return items


def is_item(li_elt):
    return li_elt.has_attr('data-sku')


def extract_item(li_elt, brand):
    item = dict()
    item['sku'] = li_elt['data-sku']
    item['title'] = get_title_item(li_elt)
    if not is_correct_brand(item['title'], brand):
        return None
    item['brand'] = brand
    item['price'] = get_current_price_item(li_elt)
    item['old_price'] = get_old_price_item(li_elt, item['price'])
    return item


def get_title_item(li_elt):
    return li_elt.find('div', class_='prdtBTit').contents[0].strip()


def is_correct_brand(title, brand):
    return brand.lower() in title.lower()


def get_old_price_item(li_elt, recent_price):
    price = li_elt.find('div', class_='prdtPrSt')
    if not price:
        return recent_price
    if len(price.contents) == 0:
        return recent_price
    price = price.contents[0].split(',')
    unit_price = number(price[0])
    dec_price = number(price[1])
    return unit_price + dec_price * 0.01


def get_current_price_item(li_elt):
    price = li_elt.find('div', class_='prdtPrice') \
        .find('span', class_='price')
    unit_price = number(price.contents[0])
    dec_price = number(price.find('sup').contents[0])
    return unit_price + dec_price * 0.01


def number(string):
    return int(''.join(re.findall('\d+', string)))


if __name__ == '__main__':
    items = get_all_items(['dell', 'acer'], verbose=True)
    df_items = persist_items(items)
    df_indicators = compute_indicators(df_items)
    persist_indicators(df_indicators)
    df_indicators = pandas.DataFrame.from_csv(csv_indicators)
    print('*** Indicators for Dell and Acer ***')
    print(df_indicators)
    print('The winner (brand with decrease_percentage maximum) is ?')
    print(df_indicators['decrease_percentage'].argmax())
