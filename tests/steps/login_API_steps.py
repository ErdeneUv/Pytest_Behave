from tests.utilities.api_utilities import *
from behave import given, when, then
import requests
import json

load_dotenv()
@given(u'I retrieve a valid CSRF token from "token_endpoint"')
def step_impl(context):

    context.token = get_token()


@when(u'User sends a POST request to "login_endpoint" with CSRF token, valid credentials of "{user}"')
def step_impl(context, user):

    context.response = login_by_role(context.token, user, user)
    assert context.response.status_code == 200, f"Login request failed with status code: {context.response.status_code} and \nmsg: {context.response.text}\n"
    #print(f"login response: {context.response}\n\n")
    context.data = context.response.json()
    context.csrf_token = context.data['csrf_token']
    context.logout_token = context.data['logout_token']
    context.username = user
    context.password = user


@then(u'User should receive a status code of {status_code}')
def step_impl(context, status_code):
    assert str(context.response.status_code) == status_code, f"Status code didn't match, user got {context.response.status_code}"


@then(u'User should receive an access token and logout access')
def step_impl(context):
    assert "logout_token" in context.data, "Response doesn't contain a logout token"
    assert "csrf_token" in context.data, "Response doesn't contain a csrf token"

@then(u'User successfully logs out using logout token')
def step_impl(context):
    logout_resp = logout(context.username, context.password, context.logout_token, context.csrf_token)

    assert logout_resp.status_code == 200, f"Assertion failed, got status code of {logout_resp.status_code} from logout request"

@when(u'User sends a POST request to "login_endpoint" with CSRF token, invalid credentials of "{name}" and "{password}"')
def step_impl(context, name, password ):
    context.username = name
    context.password = password

    context.response =login_with_creds("fake23Toke23en", context.username, context.password)

    context.data = context.response.json()
    context.message = context.data['message']


@then(u'user gets status code "{status_code}" and "{msg}"')
def step_impl(context, status_code, msg):
    assert str(context.response.status_code) == status_code, f"Response did not contain a valid response, instead: {context.response.status_code}"
    assert context.data["message"] == msg, f"Response did not contain a valid error msg instead: {context.data['message']}"


@when(u'User sends a POST request to "login_endpoint" with CSRF token, with missing pwd of "{user}"')
def step_impl(context, user):
    url = os.getenv('BASE_URL_API') + os.getenv("LOGIN_ENDPOINT")
    verify = get_verify()


    context.response = requests.post(
        url=url,
        headers={"Content-Type": "application/json",
                 "X-CSRF-Token": context.token},
        data=json.dumps({
            "name": os.getenv('USERNAME_' + user)

        }),
        verify=verify
    )
    context.data = context.response.json()



@when(u'User sends a POST request to "login_endpoint" with INVALID CSRF token, VALID credentials of "{user}"')
def step_impl(context, user):
    invalid_token = "fake234tokenlsfjo"

    context.response = login_by_role(invalid_token, user, user)
    context.data = context.response.json()

@then(u'User gets status code {status_code}')
def step_impl(context, status_code):
    assert str(context.response.status_code) == status_code, f"Response did not contain a valid status code, instead: {context.response.status_code}"


@given(u'"{user}" successfully logins with valid creds')
def step_impl(context, user):
    context.token = get_token()
    context.name = user
    context.password = user
    context.response = login_by_role(context.token, context.name, context.password)
    context.data = context.response.json()
    context.csrf_token = context.data["csrf_token"]


@when(u'"{user}" sends a GET request to "logout_endpoint" without the logout token')
def step_impl(context, user):
    url = os.getenv('BASE_URL_API') + os.getenv("LOGOUT_ENDPOINT")
    verify = get_verify()
    context.token = get_token()
    username = os.getenv('USERNAME_' + user)
    password = os.getenv('PWD_' + user)

    context.response = requests.get(
        url=url,
        headers={"Content-Type": "application/json",
                 "X-CSRF-Token": context.token,
                 "Authorization": f"Basic {get_basic(username, password)}"},
        verify = verify
    )
    context.data = context.response.json()


@given(u'User successfully logs out using logout token')
def step_impl(context):
    context.logout_token = context.data["logout_token"]
    context.response = logout(context.name, context.password, context.logout_token, context.csrf_token)


@when(u'User try to access another protected API using the previous access token')
def step_impl(context):
    access_token = context.data['csrf_token']
    context.response = build_link(access_token, 'USER', 'USER', 'www.walmart.com', 'false')



@then(u'User should receive status code 401 Unauthorized')
def step_impl(context):
    expected_status = 401
    actual_status = context.response.status_code
    context.logger.info(f'Status Code: {context.response.status_code}\n\n')