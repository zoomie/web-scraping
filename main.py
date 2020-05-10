import csv
import requests
from bs4 import BeautifulSoup


def get_all_property_links(url):
    base_url = 'https://www.pamgolding.co.za'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    page_links = []
    for list_item in soup.find_all(class_='property-contents'):
        try:
            end_path = list_item.find('a')['href']
            full_path = base_url + end_path
            page_links.append(full_path)
        except Exception as e:
            print(e)
    return page_links


def get_pages_urls():
    all_house_urls = []
    for i in range(2, 3): # 29
        list_page_list = f'https://www.pamgolding.co.za/property-search/properties-for-sale-st-francis-bay/311/page{i}'
        print(f'Getting for {i}')
        house_urls = get_all_property_links(list_page_list)
        all_house_urls.extend(house_urls)
    return all_house_urls


def get_property_info(page_link):
    page = requests.get(page_link)
    soup = BeautifulSoup(page.text, 'html.parser')
    image_path = soup.find(class_='mainImage').find('img')['src']
    price_raw = soup.find(class_='propertyInfoWrapper').find(class_='totalVal')
    price = price_raw.text.replace(' ', '').replace('\r', '').replace('\n', '')
    address = soup.find(class_='address-text').text
    if address:
        return {'price': price,
                'address': address,
                'image_path': image_path,
                'page_link': page_link}
    else:
        print(f'Unable to get property address for link: {page_link}')


with open('/Users/andrew/work/scrape_pgp_links/data.csv', 'w', newline='') as csvfile:
    fieldnames = ['price', 'address', 'page_link', 'image_path']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    all_urls = get_pages_urls()
    for i, page_link in enumerate(all_urls):
        print(f'processing {i}')
        single_dict = get_property_info(page_link)
        if single_dict:
            writer.writerow(single_dict)
