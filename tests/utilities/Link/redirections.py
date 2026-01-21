import csv
import os
import pandas as pd
from dotenv import load_dotenv
import requests
import re
from fake_useragent import UserAgent

from tests.pages.promo_page import PromoPage
from tests.utilities.final_url import by_qmark

"""if it got 401 Unauthorized Make sure the GSheet is shared publicly"""
#getting redirection needs deeplink, and target url, and status code
def get_location(url, p_url):
    session = requests.Session()
    session.max_redirects = 6
    is_redir = True
    redirections = []

    while is_redir:
        print(f"'\u001b[32m' STARTING>> {url} '\u001b[0m'")
        redirections.append(url)

        if 'NOT_Supported' in url:
            redirections.append("https://www.target.com/NOT_Supported.com")
            print("NOT SUPPORTED DETECTED>>>>>>>")
            break
        else:
            try:
                response = requests.get(url, allow_redirects=False)
                if response.headers.__contains__('Location'):
                    location = response.headers['Location']
                    location_split = by_qmark(location)
                    print(f'LOCATION_SPLIT: {location_split} >>> ')

                    p_url_split = by_qmark(p_url)
                    print(f'p_url_split: {p_url_split}')

                    if location_split not in  p_url_split:
                        redirections.append(response.status_code)
                        redirections.append(location)
                        print(f'Location is not a match: {location_split}')
                        url = location
                    else:
                        redirections.append(response.status_code)
                        redirections.append(location)
                        print(f'LOCATION IS MATCH: {location_split}\n\n')
                        redirections.append('200')
                        #presumed it landed on product link so added status code 200
                        break

                elif response.headers.__contains__('Refresh'):
                    refresh: str = response.headers['Refresh'].split('0; url=')[1]
                    redirections.append(response.status_code)
                    redirections.append(refresh)
                    url = refresh
                else:
                    """Try getting payload and look for key that contains 'link' """
                    data = response.json()
                    if 'link' in data:
                        redirections.append(response.status_code)
                        redirections.append(data['data'])
                    is_redir = False
                    print("ELSE")
                    print(f'Headers: {response.headers}')
                    break
            except Exception as e:
                redirections.append([f"Error: {e}"])
                print(f'Error occurred on: {url} with {e}')
        print(f"REDIRECTIONS: {redirections}\n")
    return redirections


def mavely(url, p_url):
    session = requests.Session()
    session.max_redirects = 16
    user_agents = UserAgent()
    user_str = user_agents.chrome
    session.headers.update({'User-Agent': user_str})

    is_redir = True
    redirections = []

    print(f"'\u001b[32m' STARTING>> {url} '\u001b[0m'")

    if 'NOT_Supported' in url:
        redirections.append("https://www.target.com/NOT_Supported.com")
        print("NOT SUPPORTED DETECTED>>>>>>>")
    elif 'www.michaelkors.com' in url:
        redirections.append("https://www.target.com/NOT_Supported.com")
        print("NOT SUPPORTED DETECTED>>>>>>>")

    else:
        try:

            response = session.get(url, allow_redirects=True)
            print(f'HISTORY: {response.history}')
            # getting 'Locations' headers and it's status
            for resp in response.history:
                print(f'FRESH: {resp.headers}')
                entry = f'{resp.url}, {resp.status_code}'
                print(f'LOCATIONS: {resp.url}')

                # getting 'Refresh' headers and it's status
                if 'Refresh' in resp.headers:
                    refresh_header: str = response.headers['Refresh'].split('0; url=')[1]
                    entry += f'{refresh_header}, {resp.status_code}'

                # adding final url and status
                entry += f', {response.url}, {response.status_code}'

                redirections.append(entry)
        # if there is any problem it will save the error
        except Exception as e:
            redirections.append([f"Error: {e}"])
            print(f'Error occurred on: {url} with {e}')
    print(f"REDIRECTIONS: {redirections}\n")
    return redirections







# slicing url by '?' and takes what comes before '?'
def slicing(url):
    return url.split('?')[0]

def redirections_to_csv(file_name, product_links, deeplinks):
    file_name = file_name if file_name.endswith('.csv') else file_name + '.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Product_URL', 'Deep Link', 'Redirection_1', 'Redirection_2', 'Redirection_3',...,])
        for url, link in zip(product_links, deeplinks):
            writer.writerow([url] + link) #use all_redirections here
    print("CSV File has been WRITTEN '\u001b[0m'")

def open_gsheet(gid):
    # accessing gsheet and getting Product URLs or deeplinks
    load_dotenv()
    sheet_id = os.getenv('gsheet_id')
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv{gid}")
    return df



if __name__ == '__main__':
    all_redirections = []
    gid = ('&gid=327777343'
           '') #Change this if it's not first sheet. Don't forget to start with &

    df = open_gsheet(gid)
    deep_links = df["Deep Link"]
    product_urls = df["Product URL"]
    is_redir = True

#Taking a Product URL and a LTK Link then follows LTK Link to collect it's redirect while checking if it match the Product URL. if it matches it would stop redirection, making sure not being detected by bot detection. It stores all those redirections URL to redirections list and after it breaks away from the loop it would store redirections list to all_redirections list. Then it would create redirection.csv and store all_redirections list in it
    print(f'DeepLinks: {deep_links}')
    for link, p_url in zip(deep_links, product_urls):
        redirections = []
        all_redirections.append(mavely(link, p_url))
    redirections_to_csv('redirections.csv', product_urls, all_redirections)


