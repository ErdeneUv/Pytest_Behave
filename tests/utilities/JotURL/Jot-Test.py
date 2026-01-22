import json
import os
import urllib.parse

import requests
import pandas as pd
from dotenv import load_dotenv
from tests.utilities.api_utilities import get_token, login_with_creds, build_link, logout


def get_bc_links():

    load_dotenv()
    # variables
    env = 'prod'
    username = 'user'
    password = 'user_prod'

    # getting token
    token = get_token()

    # logging in
    login_body = login_with_creds(token, username, password).json()
    csrf_token_jot = login_body['csrf_token']
    logout_token_jot = login_body['logout_token']

    # getting urls from excel
    # Get the directory where JTest.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path to the Excel file
    file_path = os.path.join(current_dir, "links.xlsx")
    df = pd.read_excel(file_path, sheet_name='Jot', engine='openpyxl')
    product_urls = df['product_urls']
    # deleting excess rows beyond 15.
    total_rows = len(df)
    if total_rows > 15:
        df = df.head(15)
    df.to_excel(file_path, sheet_name='Jot', index=False, engine='openpyxl')

    # building  BC links
    aff_links = []
    for url in product_urls:
        link = build_link(csrf_token_jot, env, username, password, url, 'false').json()['url']
        aff_links.append(link)

    # editing BC links
    cohort_a = []
    cohort_b = []
    for url in aff_links:
        # use jot_cohort_a_standard for real test
        url = url + '&aff_sub4=jot_cohort_a_standard'
        cohort_a.append(url)
    print(f'COHORT_A: {cohort_a}')

    for url in aff_links:
        # use jot_cohort_b_deeplink for real test
        url = url + '&aff_sub4=jot_cohort_b_deeplink'
        cohort_b.append(url)
    print(f'COHORT_A: {cohort_b}')

    # writing BC links
    index = 0
    for link in cohort_a:
        df.at[index, 'Cohort_A'] = link
        index += 1
    index = 0
    for link in cohort_b:
        df.at[index, 'Cohort_B'] = link
        index += 1
    print('WRITING TO Excel')
    df.to_excel(file_path, sheet_name='Jot', index=False, engine='openpyxl')

    # logging out from platform
    logged_out = logout(env, username, password, logout_token_jot, csrf_token_jot)


def urls_shorten(long_url):
    #to create a normal joturl link we need two, each for cohort_a, b

    project_id = 'bc_jot'
    url = f'https://joturl.com/a/i1/urls/shorten?&project_id={project_id}&long_url={long_url}'
    token = os.getenv('JOT_TOKEN')

    response = requests.get(
        url= url,
        headers={
            'Authorization': f'Bearer {token}'
        }
                            ).json()
    return response

def urls_easy_info(id):
    #get information regarding tracking link for easy deep-link, edl
    token = os.getenv('JOT_TOKEN')
    url = f'https://joturl.com/a/i1/urls/easydeeplinks/info?id={id}'
    response = requests.get(
        url=url,
        headers={
            'Authorization': f'Bearer {token}'
        }
    ).json()
    return response

def urls_easy_edit(t_id, t_settings):
    #creating edl
    token = os.getenv('JOT_TOKEN')
    url = f'https://joturl.com/a/i1/urls/easydeeplinks/edit?id={t_id}&settings={t_settings}'
    response = requests.post(
        url=url,
        headers={
            'Authorization': f'Bearer {token}'
                }
    ).json()
    return response

def urls_balancer_edit(t_id,urls):
    #add balancer to normal link with edl
    token = os.getenv('JOT_TOKEN')
    type = 'WEIGHTED_FIXED'
    weights = [50.00, 50.00]
    url = f'https://joturl.com/a/i1/urls/balancers/edit?id={t_id}&type={type}&urls={urls}&weights={weights}'

    response = requests.get(
        url=url,
        headers={
            'Authorization': f'Bearer {token}'
        }
    ).json()
    return response


def get_bc_shorts(cohort):
    # getting short_cohort_a and b from excel
    cohort_result = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "links.xlsx")
    df = pd.read_excel(file_path, sheet_name='Jot', engine='openpyxl')
    if 'cohort_a' in cohort:
        cohort_result = df['short_cohort_a'].iloc[0:].tolist()
    if 'cohort_b' in cohort:
        cohort_result = df['short_cohort_b'].iloc[0:].tolist()
    return cohort_result

if __name__ == '__main__':

    # I needed to create each long links a short ones, I didn't have access token to the api so manually creating short urls and saving them in the google sheet/xlsx sheet. here is the array holding them

    # need to use pandas and get short links in perspective arrays
    short_cohort_a = get_bc_shorts('cohort_a')
    short_cohort_b = get_bc_shorts('cohort_b')

    # will create jot links out of all short_cohort and store them in jot_cohort_b and their tracking ids in jot_cohort_b_tracking_id
    jot_cohort_b = []
    jot_cohort_b_tracking_id = []
    jot_cohort_a = []
    jot_cohort_a_tracking_id = []

    # creating normal joturl link out of cohort_b
    for short_b in short_cohort_b:
        print(f"SHORT THAT IS USED: {short_b}")
        short_b_data = urls_shorten(short_b)

        jot_cohort_b.append(short_b_data['result']['short_url'] )
        jot_cohort_b_tracking_id.append(short_b_data['result']['id'])

    #creating jot_cohort_b edl links
    for tracking_id in jot_cohort_b_tracking_id:
        tracking_data = urls_easy_info(tracking_id)
        settings = tracking_data['result']
        settings_data = json.dumps(settings)
        data = urllib.parse.quote(settings_data)

        edl_enabled = urls_easy_edit(tracking_id, data)
        print(f'EASY_ENABLED_COHORT_B: {edl_enabled}\n')

    # writing edl links to joturl_edl column in excel
    # Get the directory where JTest.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path to the Excel file
    file_path = os.path.join(current_dir, "links.xlsx")
    df = pd.read_excel(file_path, sheet_name='Jot', engine='openpyxl')

    index = 0
    for link_b in jot_cohort_b:
        df.at[index, 'joturl_edl'] = link_b
        index += 1
    df.to_excel(file_path, sheet_name='Jot', index=False, engine='openpyxl')

    # creating normal out of cohort_a
    for short_a in short_cohort_a:
        short_a_data = urls_shorten(short_a)
        jot_cohort_a.append(short_a_data['result']['short_url'] )
        jot_cohort_a_tracking_id.append(short_a_data['result']['id'])
    print(f'JOT_COHORT_A DATA: {jot_cohort_a}\n')

    # writing jot_cohort_a normal links to the excel file
    df = pd.read_excel(file_path, sheet_name='Jot', engine='openpyxl')
    index = 0
    for link_a in jot_cohort_a:
        df.at[index, 'joturl_normal'] = link_a
        index += 1
    df.to_excel(file_path, sheet_name='Jot', index=False, engine='openpyxl')


    # adding balancer to cohort_a normal link with cohort_b edl links
    for tracking, cohort_a, cohort_b in zip(jot_cohort_a_tracking_id, jot_cohort_a, jot_cohort_b):
        dest_urls = json.dumps([cohort_a, cohort_b])
        is_balanced = urls_balancer_edit(tracking, dest_urls)
        print(f'ADDING BALANCER: {is_balanced}')
