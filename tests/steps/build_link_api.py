import logging

import requests.exceptions
from tests.utilities.api_utilities import *
from behave import when, then
from tests.utilities.final_url import fin_url, q_fin_url
from tests.utilities.url_assertion import url_assertion

logger = logging.getLogger()


@when(u'user sends supported brand "{url}" to build link api with valid credentials and access token')
def step_impl(context, url):
    is_short = False
    context.url = os.getenv(url)
    #logger.info(f"\n{context.url} is sent to /deeplinking\n")
    context.res = build_a_link_no_login(context.url, is_short)


@then(u'user gets status code "{200}", "{url}" and "{url_long}" url brandcycle links')
def step_impl(context, status_code, url, url_long):
    assert str(context.res.status_code) == status_code, f"Status code is not equal to expected, instead {context.res.status_code} and got msg {context.res.text}"
    body = context.res.json()
    context.long_url = body['url_long']
    print(f'Link created: {context.long_url}\n')




@when("user send get request to BC link")
def step_impl(context):
    context.current_url = q_fin_url(context.long_url, context.url)

@then("the user should see Brand url in final response")
def step_impl(context):
    url_assertion(context.url, context.current_url)
    context.current_url = ''


@when(u'user sends "{url}" to build link api with valid credentials and access token')
def step_impl(context, url):
    is_short = "false"
    context.brand_url = os.getenv(url)
    context.res = build_a_link_no_login(context.brand_url, is_short)
    print(f'no deeplink: {context.res}\n {context.res.status_code}\n{context.res.text}')


@then(u'user should get status code "{status_code}" and "{msg}" msg')
def step_impl(context, status_code, msg):
    body = context.res.json()
    actual_msg = body['message']
    assert str(context.res.status_code) == status_code, f"Status code is not equal to expected, instead {context.res.status_code}"

    assert actual_msg == msg, f'Body doesnt contain msg, instead:  {body["message"]}'


@when(u'user sends blacklisted "{brand_url}" to build link api with valid credentials and access token')
def step_impl(context, brand_url):
    is_short = "true"
    context.brand_url = os.getenv(brand_url)
    context.res = build_a_link_no_login(context.brand_url, is_short)


@when(u'user sends "{whitelisted_private_brand_url}" to to build link api with INVALID credentials and access token')
def step_impl(context, whitelisted_private_brand_url):
    url = os.getenv('BASE_URL_API')
    verify = get_verify()

    is_short = "true"
    context.brand_url = os.getenv(whitelisted_private_brand_url)

    username = "test_user"
    password = "Super_secret_password"
    access_token = get_token()

    context.res = requests.post(
        url=url + os.getenv("BUILD_ENDPOINT"),
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "csrf_token": access_token,
                 "Authorization": f"Basic {get_basic(username, password)}"},
        data={
            "targetUrl": whitelisted_private_brand_url,
            "shortLink": is_short,
        },
        verify=verify
    )


@then(u'user should get "{status_code}" and "{msg}" msg')
def step_impl(context, status_code, msg):
    actual_msg = context.res.json()

    assert str(
        context.res.status_code) == status_code, f"Status code is not equal to expected, instead {context.res.status_code}"

    assert actual_msg == msg, f'Body doesnt contain msg, instead:  {actual_msg}'

@when(u'user sends request without urls to build link api with valid credentials and access token')
def step_impl(context):
    url = os.getenv('BASE_URL_API') + os.getenv("BUILD_ENDPOINT")
    verify = get_verify()

    token = get_token()
    login_resp = login_by_role(token, 'USER', 'USER')
    csrf_token = login_resp.json()['csrf_token']
    logout_token = login_resp.json()['logout_token']
    username = os.getenv('USERNAME_USER')
    password = os.getenv('PWD_USER')
    print(f'issue: {csrf_token}, {logout_token}\n\n\n')
    context.res = requests.post(
        url= url,
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "csrf_token": csrf_token,
                   "Authorization": f"Basic {get_basic(username, password)}"},
        data = {
            "shortLink": 'false'
        },
        verify = verify
    )
    print(f'no deeplink: {context.res}\n {context.res.status_code}\n{context.res.text}\n\n')
