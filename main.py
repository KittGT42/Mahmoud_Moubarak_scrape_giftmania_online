import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

headers_csv = ['Product_Name', 'Product_Categorise', 'Product_price', 'Product_Images']

today_day_data = f'_{datetime.now().day}_{datetime.now().month}_{datetime.now().year}'
with open(f'detailed_info_product{today_day_data}.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers_csv)

stock_url = 'https://giftmania.online'
categories_urls = ['https://giftmania.online/collections/figures', 'https://giftmania.online/collections/games-more',
                   'https://giftmania.online/collections/accessories',
                   'https://giftmania.online/collections/decorations',
                   'https://giftmania.online/collections/funko', 'https://giftmania.online/collections/music-boxes']

for category_url in categories_urls:
    for i in range(100):
        res = requests.get(f'{category_url}?page={i}')
        soup = BeautifulSoup(res.content, 'lxml')
        name_category = soup.find('h1', class_='collection-hero__title').contents[2]
        all_product_links_from_page = soup.find_all('li', class_='grid__item scroll-trigger animate--slide-in')
        if len(all_product_links_from_page) > 0:
            for link in all_product_links_from_page:
                res_product_link = requests.get(stock_url + (link.find('a').get('href')))
                soup_product_link = BeautifulSoup(res_product_link.content, 'lxml')
                product_name = soup_product_link.find('div', class_='product__title').find('h1').text
                product_price = soup_product_link.find('span', class_='price-item price-item--regular').text.replace(
                    '\n', '').strip(' ')
                product_images = soup_product_link.find_all('img', class_='image-magnify-lightbox')

                product_images_list = []
                for image in product_images:
                    product_images_list.append('https:' + image.get('src'))

                with open(f'detailed_info_product{today_day_data}.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([product_name, name_category, product_price, product_images_list])

                print('Downloaded: ', product_name, 'Page: ', i)
        else:
            print(f'No products in this page {i}')
