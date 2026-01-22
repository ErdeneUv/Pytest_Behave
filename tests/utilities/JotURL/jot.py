import json
import os
import time

import requests
import hmac
import hashlib
from datetime import datetime
from dotenv import load_dotenv
import urllib.parse

from pandas.core.config_init import pc_max_info_rows_doc

load_dotenv()

def get_hmac(private_key="", message=""):
    #message is the public key
    gmt_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')
    message += f":{gmt_datetime}"

    return hmac.new(str.encode(private_key), str.encode(message), hashlib.sha256).hexdigest()

def jot_login(email, private_key, public_key):

    password_hash = get_hmac(private_key, public_key)
    url = f"https://joturl.com/a/i1/users/login?username={email}&password={password_hash}"

    response = requests.get(url).json()

    if "result" in response and "session_id" in response["result"]:
        return response["result"]["session_id"]
    else:
        raise ValueError("Unexpected response format: " + str(response))

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
    weights = [50.00,50.00]
    url = f'https://joturl.com/a/i1/urls/balancers/edit?id={t_id}&type={type}&urls={urls}&weights={weights}'

    response = requests.get(
        url=url,
        headers={
            'Authorization': f'Bearer {token}'
        }
    ).json()
    return response


if __name__ == '__main__':
    #to create a normal tracking link to the destination
    #long_cohort_a_link = 'https://br.go2cloud.org/aff_c?offer_id=33&aff_id=29&url=https%3A%2F%2Fadidas.njih.net%2Fc%2F193465%2F264102%2F4270%3FsubId1%3DA{affiliate_id}O{offer_id}TID{transaction_id}%26sharedid%3D{affiliate_id}%26u%3Dhttps%253A%252F%252Fwww.adidas.com%252Fus%252Fultraboost-1.0-fortnite-shoes%252FJQ0717.html%253Fpr%253Dtaxonomy_rr%2526slot%253D1%2526rec%253Dmt&aff_unique3=e6aea3d5-cd09-46c7-b8bb-b3512fc64d86&aff_sub4=cohort_a'
    short_cohort_a='https://br.link/0xyj9'
    short_cohort_b= 'https://www.kohls.com/product/prd-6615558/bobs-by-skechers-hands-free-slip-ins-skipper-keep-it-classic-womens-shoes.jsp?prdPV=18&isClearance=false'
    #long_cohort_b_link = 'https://br.go2cloud.org/aff_c?offer_id=33&aff_id=29&url=https%3A%2F%2Fadidas.njih.net%2Fc%2F193465%2F264102%2F4270%3FsubId1%3DA{affiliate_id}O{offer_id}TID{transaction_id}%26sharedid%3D{affiliate_id}%26u%3Dhttps%253A%252F%252Fwww.adidas.com%252Fus%252Fultraboost-1.0-fortnite-shoes%252FJQ0717.html%253Fpr%253Dtaxonomy_rr%2526slot%253D1%2526rec%253Dmt&aff_unique3=e6aea3d5-cd09-46c7-b8bb-b3512fc64d86&aff_sub4=cohort_b'

    short_start_time = time.time()
    #creating normal joturl link out of cohort_b
    jot_link_data = urls_shorten(short_cohort_b)
    short_end_time = time.time()
    short_time = round(short_end_time - short_start_time, 2)
    #print(f'JOTURL_B: {jot_link_data}\n')
    jot_link_b = jot_link_data['result']['short_url']
    tracking_id_b = jot_link_data['result']['id']
    print(f'NORMAL JOT URL COHORT B TRACKING ID {tracking_id_b}\n JOT_LINK_B: {jot_link_b}\n')
    print(f"/shorten: {short_time}")

    start_info = time.time()
    #to extract the information regarding the tracking link
    tracking_resp = urls_easy_info(tracking_id_b)
    end_info = time.time()
    info_time = round(end_info - start_info, 2)
    print(f"/info: {info_time}")
    settings = tracking_resp['result']
    data = json.dumps(settings)
    data = urllib.parse.quote(data)

    #making cohort_b normal link above an edl
    edl_start_time = time.time()
    easy_enabled = urls_easy_edit(tracking_id_b, data)
    edl_end_time = time.time()
    edl_time = round(edl_end_time - edl_start_time, 2)
    print(f"/edit: {edl_time}")
    total = short_time + info_time + edl_time
    print(f"TOTAL: {round(total, 2)}")
    print(f'EASY_ENABLED_COHORT_B: {easy_enabled}\n')


  #creating normal out of cohort_a
    short_2_start = time.time()
    jot_cohort_a_data = urls_shorten(short_cohort_a)
    short_2_end = time.time()
    short_2_time = short_2_end-short_2_start
    tracking_id_a = jot_cohort_a_data['result']['id']
    jot_link_a = jot_cohort_a_data['result']['short_url']
    print(f'JOT_LINK_A: {jot_link_a}\n')

    # adding balancer to cohort_a normal link with cohort_b edl links
    balancer_start = time.time()
    dest_urls = json.dumps([short_cohort_a, jot_link_b])
    is_balanced = urls_balancer_edit(tracking_id_a, dest_urls)
    balancer_end = time.time()
    balancer_time = balancer_end - balancer_start
    print(f"/short for cohort_a: {round(short_2_time, 2)}")
    print(f"/balancer: {round(balancer_time, 2)}")
    grand_total = round(total + short_2_time + balancer_time, 2)
    print(f"GRAND TOTAL: {grand_total}")
    print(f'ADDING BALANCER: {is_balanced}')




"""
    get jot api token from https://joturl.com/reserved/settings.html#tools-api 
    
    JOT_LINK_B: https://jo.my/96f980fc
    
    JOT_LINK_A: https://jo.my/5a54350e
        clicks on JOT_LINK_A:
            march 28:
            1027 - work laptop
            1029 - personal iphone
            1029 - window laptop
            1030 - S21
            1032 - ipad01
            1033 - ipad02
            1036 - s23
            1038 - iphone
                
    """
