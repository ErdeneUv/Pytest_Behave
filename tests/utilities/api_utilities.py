import json
import os
from time import sleep

import requests
import base64
from dotenv import load_dotenv
import certifi

session = requests.Session()
load_dotenv()


def get_verify():
    env = os.getenv("ENVIRONMENT")
    if env == 'local':
        verify_p = os.getenv("CA_PATH")
    else:
        verify_p = certifi.where()
    return verify_p


def get_basic(username, password):
    # pwd should tell which env and role it wants: user_prod
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode("utf-8")).decode()
    return encoded


def get_token():
    verify = get_verify()
    url = os.getenv('BASE_URL_API') + os.getenv('TOKEN_ENDPOINT')
    return requests.get(
        url=url,
        verify=verify
    ).text


def login_by_role(token, username, password):
    # pwd should tell which env and role it wants: user_prod
    url = os.getenv('BASE_URL_API') + os.getenv("LOGIN_ENDPOINT")
    verify = get_verify()
    username = os.getenv('USERNAME_' + username)
    password = os.getenv('PWD_' + password)
    response = requests.post(
        url=url,
        headers={"Content-Type": "application/json",
                 "X-CSRF-Token": token},
        data=json.dumps({
            "name": username,
            "pass": password
        }),
        verify=verify
    )
    return response


def login_with_creds(token, username, pwd):
    # this function will use passed username and pwd directly
    url = os.getenv('BASE_URL_API') + os.getenv("LOGIN_ENDPOINT")
    verify = get_verify()
    response = requests.post(
        url=url,
        headers={"Content-Type": "application/json",
                 "X-CSRF-Token": token},
        data=json.dumps({
            "name": username,
            "pass": pwd
        }),
        verify=verify
    )
    return response


def logout(username, password, logout_token, csrf):
    url_base = os.getenv('BASE_URL_API' )
    verify = get_verify()
    username = os.getenv('USERNAME_' + username)
    password = os.getenv('PWD_' + password)

    complete_url = url_base + os.getenv('LOGOUT_ENDPOINT') + logout_token
    response = requests.get(
        url=complete_url,
        headers={"Content-Type": "application/json",
                 "csrf_token": csrf,
                 "Authorization": f"Basic {get_basic(username, password)}"},
        verify=verify
    )
    return response


def build_link(csrf_token, username, password, target_url, short_link):
    url = os.getenv('BASE_URL_API') + os.getenv("BUILD_ENDPOINT")
    #logger = logging.getLogger()
    #logger.info(f'API calls are sent to... {url}\n\n')
    verify = get_verify()
    username = os.getenv('USERNAME_' + username)
    password = os.getenv('PWD_' + password)
    response = requests.post(
        url=url,
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "csrf_token": csrf_token,
                 "Authorization": f"Basic {get_basic(username, password)}"},
        data={
            "targetUrl": target_url,
            "shortLink": short_link
        },
        verify=verify
    )
    return response


def build_a_link_no_login(target_url, is_short):
    token = get_token()
    login_resp = login_by_role(token, 'USER', 'USER')
    access_token = login_resp.json()['csrf_token']
    build_resp = build_link(access_token, 'USER', 'USER', target_url, is_short)
    return build_resp


def get_active_brands_id(username, pwd, access_token):
    url = os.getenv('BASE_URL_API') + os.getenv("BRANDS_LIST")
    #print(f'API calls are sent to... {url}\n\n')
    verify = get_verify()

    active_brands_resp = requests.get(
        url=url,
        headers={
            #"Content-Type": "application/x-www-form-urlencoded",
            "csrf_token": access_token,
            "Authorization": f"Basic {get_basic(username, pwd)}"
        },
        verify=verify
        ).json()
    #print(f'active_brands_resp: {active_brands_resp}\n\n\n')
    active_brands = active_brands_resp["brandsSelect"]
    active_brands_id = [item["id"] for item in active_brands]
    return active_brands_id


def get_br_details_by_id(username, pwd, access_token, brand_id):
    endpoint = os.getenv("BRANDS_DETAILS")
    final_endpoint = endpoint.replace("1401", str(brand_id))
    url = os.getenv('BASE_URL_API') + final_endpoint
    verify = get_verify()

    brands_detail_resp = requests.get(
        url=url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "csrf_token": access_token,
            "Authorization": f"Basic {get_basic(username, pwd)}"
        },
        verify=verify
    ).json()
    sleep(1)
    return brands_detail_resp


def get_br_homepage_url(username, pwd, access_token, brand_id):
    try:
        brand_detail_resp = get_br_details_by_id(username, pwd, access_token, brand_id)
        #print(f'ID TO GET DETAILS: {id}\n')
        #print(f'brand_detail_resp: {brand_detail_resp}\n\n\n')
        print(f'GET_HP_URLS BR_DETAILS of {brand_id}:')
        sleep(1)
        if isinstance(brand_detail_resp, dict):
            homepage_url = brand_detail_resp['info']['url']
            print(f'{homepage_url}\n\n')
            return homepage_url
        else:
            print(f"Invalid ID is sent: {brand_id}\nResponse was:{brand_detail_resp}\n")
            return None
    except Exception as e:
        print(f'Invalid ID: {e}\n')
        return None


def get_bc_link_from_detail(username, pwd, access_token, brand_id):
    brands_detail_resp = get_br_details_by_id(username, pwd, access_token, brand_id)
    sleep(1)
    if isinstance(brands_detail_resp, dict) and brands_detail_resp['info']['enableDeepLinking'] == 0:
        bc_link =  brands_detail_resp['info']['longLink']
        return bc_link
    else:
        bc_link = get_homepage_bc_link(username, pwd, access_token, brand_id)
        return bc_link


def get_homepage_bc_link(username, pwd, access_token, brand_id):
    username = os.getenv('USERNAME_' + username)
    pwd = os.getenv('PWD_' + pwd)
    endpoint = os.getenv("HOMEPAGE_DEEPLINK")
    final_endpoint = endpoint.replace("1401", str(brand_id))
    url = os.getenv("BASE_URL") + final_endpoint
    verify = get_verify()
    try:
        resp = requests.get(
            url=url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "csrf_token": access_token,
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            verify=verify
        )
        homepage_link = resp.text
        homepage_link = json.loads(homepage_link)
        sleep(1)
        return homepage_link
    except Exception as e:
        print(f"Invalid ID: {e}\n is this brand inactive?\n\n")

def get_dealID(keywords = "", brand_title = "- Any -", sort_by = 'start', order_by = 'new'):
    #if any of the body is not needed, then you can pass "". keywords
    username = os.getenv('USERNAME_' + 'USER')
    pwd = os.getenv('PWD_' + 'USER')
    endpoint = os.getenv('DEAL_ID_ENDPOINT')
    url = os.getenv('BASE_URL_API') + endpoint
    verify = get_verify()
    try:
        resp = requests.post(
            url=url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            verify=verify,
            data={
                "page": 1,
                "keywords": keywords,
                "brandTitle" : brand_title,
                "sortBy" : sort_by,
                "orderBy" : order_by
            }
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")


def get_promo_link(deal_id):
    username = os.getenv('USERNAME_' + 'USER')
    pwd = os.getenv('PWD_' + 'USER')

    endpoint = os.getenv('PROMO_ENDPOINT')
    endpoint = endpoint.replace("dealID", str(deal_id))
    url = os.getenv('BASE_URL_API') + endpoint
    verify = get_verify()
    try:
        resp = requests.get(
            url=url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")


def get_subusers(user):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('SUBUSERS')
    url = os.getenv('BASE_URL_API') + endpoint
    verify = get_verify()
    try:
        resp = requests.get(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")


def get_engaged_brands(userID):
    username = os.getenv('USERNAME_' + "USER")
    pwd = os.getenv('PWD_' + "USER")
    endpoint = os.getenv('BRANDS_ENGAGED')
    endpoint = endpoint.replace("12781", str(userID))
    url = os.getenv('BASE_URL_API') + endpoint
    verify = get_verify()
    try:
        resp = requests.get(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def get_lpr(user, user_id, brand_id=None, period_start=None, period_end=None, sort=None, direction=None):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('LINK_PERFORMANCE')
    url = os.getenv('BASE_URL_API') + endpoint
    verify = get_verify()

    params = {"userId": user_id }
    if brand_id is not None:
        params["brandId"] = brand_id
    if period_start is not None:
        params["periodStart"] = period_start
        params["periodEnd"] = period_end
    if sort is not None:
        params["sort"] = sort
    if direction is not None:
        params["direction"] = direction
    try:
        resp = requests.get(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            params=params,
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def get_product_info(destination_url):
    username = os.getenv('USERNAME_' + 'USER')
    pwd = os.getenv('PWD_' + 'USER')
    endpoint = os.getenv('PRODUCT_INFO')
    url = os.getenv('BASE_URL_BC_API') + endpoint
    verify = get_verify()
    api_secret = os.getenv('X_API_SECRET')
    payload = {"destinationUrl": destination_url}
    try:
        resp = requests.post(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}",
                "x-api-secret": api_secret,
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            verify=verify,
            json=payload
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def create_collection(user_id, name, description, image_url=None, status="draft", user="USER"):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION')
    url = os.getenv('BASE_URL_API') + endpoint
    verify = get_verify()
    payload = {
        "data": {
            "type": "collection",
            "attributes": {
                "userId": user_id,
                "name": name,
                "description": description,
                "defaultImageUrl": image_url,
                "status": status
            }
        }
    }
    try:
        resp = requests.post(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json=payload,
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def get_collection_for_user(user_id, user="USER", status: str | None = None):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION')
    url = os.getenv('BASE_URL_API') + endpoint + '?userId=' + user_id
    if status:
        url += f"&status={status}"
    verify = get_verify()
    try:
        resp = requests.get(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def get_collection_for_collection(collection_id, user="USER"):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION')
    url = os.getenv('BASE_URL_API') + endpoint + '/' + collection_id + '/items'
    verify = get_verify()
    try:
        resp = requests.get(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def update_collection(collection_id, name=None, description=None, status=None, user="USER"):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION')
    url = os.getenv('BASE_URL_API') + endpoint + '/' + collection_id
    verify = get_verify()
    attributes = {}
    payload = {
        "data": {
            "type": "collections",
            "attributes": attributes
        }
    }
    if name is not None:
        attributes['name'] = name
    if description is not None:
        attributes['description'] = description
    if status is not None:
        attributes['status'] = status

    try:
        resp = requests.patch(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json=payload,
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def delete_collection(collection_id, user="USER"):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION')
    url = os.getenv('BASE_URL_API') + endpoint + '/' + collection_id
    verify = get_verify()
    try:
        resp = requests.delete(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}",
            },
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def create_collection_item(collection_id, name, original_url, shopping_url, store, image_url, user="USER"):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION_ITEMS')
    url = os.getenv('BASE_URL_API') + endpoint
    verify = get_verify()
    attributes = {}
    payload = {
        "data": {
            "type": "collections_items",
            "attributes": attributes
        }
    }
    if collection_id is not None:
        attributes['collectionId'] = collection_id
    if name is not None:
        attributes['name'] = name
    if original_url is not None:
        attributes['originalUrl'] = original_url
    if shopping_url is not None:
        attributes['shoppingUrl'] = shopping_url
    if store is not None:
        attributes['store'] = store
    if image_url is not None:
        attributes['imageUrl'] = image_url
    try:
        resp = requests.post(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json=payload,
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def get_collection_item(collection_item_id, user="USER"):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION_ITEMS')
    url = os.getenv('BASE_URL_API') + endpoint + '/' + collection_item_id
    verify = get_verify()
    try:
        resp = requests.get(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}"
            },
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def update_collection_item(collection_item_id, name=None, original_url=None, shopping_url=None, store=None, image_url=None, user="USER"):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION_ITEMS') + '/' + collection_item_id
    url = os.getenv('BASE_URL_API') + endpoint
    verify = get_verify()
    attributes = {}
    payload = {
        "data": {
            "type": "collections_items",
            "attributes": attributes
        }
    }
    if name is not None:
        attributes['name'] = name
    if original_url is not None:
        attributes['originalUrl'] = original_url
    if shopping_url is not None:
        attributes['shoppingUrl'] = shopping_url
    if store is not None:
        attributes['store'] = store
    if image_url is not None:
        attributes['imageUrl'] = image_url
    try:
        resp = requests.patch(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json=payload,
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

def delete_collection_item(collection_item_id, user="USER"):
    username = os.getenv('USERNAME_' + user)
    pwd = os.getenv('PWD_' + user)
    endpoint = os.getenv('COLLECTION_ITEMS')
    url = os.getenv('BASE_URL_API') + endpoint + '/' + collection_item_id
    verify = get_verify()
    try:
        resp = requests.delete(
            url=url,
            headers={
                "Authorization": f"Basic {get_basic(username, pwd)}",
            },
            verify=verify
        )
        return resp
    except Exception as e:
        print(f"request failed: {e}\n\n")

if __name__ == '__main__':
    collection_item_id = '35'
    name = "Pumpkin and Ghost - Updated"
    shopping_url = "https://brandcycle.shop/slug1"
    store = 'walmart'
    image_url = 'https://assets.wfcdn.com/im/85043383/resize-h1200-w1200%5Ecompr-r85/1656/165662138/Pumpkin+and+Ghost+%22Boo%22+Halloween+Gel+Window+Clings.jpg'
    original_url = "https://www.wayfair.com/decor-pillows/pdp/northlight-seasonal-pumpkin-and-ghost-boo-halloween-gel-window-clings-nlgv8468.html"
    url = 'https://www.hsn.com/products/hp-100-sheet-finecut-shredder-with-38-gallon-pullout-bi/23478146'
    resp = get_product_info(url)
    print(resp.text)
    print(resp.status_code)
