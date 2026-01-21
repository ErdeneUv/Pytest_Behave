from time import sleep
from selenium.webdriver.support import expected_conditions as ec
import requests.exceptions
from selenium.webdriver.common.by import By
from tests.pages.home_page import HomePage
from tests.utilities.api_utilities import *
from behave import when, then
from tests.utilities.click_on_element import click_on_element
from selenium.webdriver import ActionChains

from tests.utilities.selenium_utilities import select_date, close_beamer

load_dotenv()
@when(u'User sends a Post request to "{reports_endpoint}" to get snapshots of November as a "{user}"')
def step_impl(context, reports_endpoint, user):
    username = os.getenv("USERNAME_" + user)
    password = os.getenv("PWD_" + user)
    url = os.getenv('BASE_URL_API') + os.getenv(reports_endpoint)
    verify = get_verify()
    access_token = get_token()

    context.response = requests.post(
        url=url,
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "csrf_token": access_token,
                 "Authorization": f"Basic {get_basic(username, password)}",
                 "_format": "json"
        },
        data={
            "type": "homepage_report",
            "data_filter": "Between Dates",
            "from_date": "2023-11-01",
            "to_date": "2024-12-31",
            "users": "all",
            "resolution": "day",
            "homepage": "true",
        },
        verify = verify
    )

@then('User should get status code "{status_code}"')
def step_impl(context, status_code):
    actual_status_code = str(context.response.status_code)
    assert actual_status_code == status_code, f'Assertion FAILED: actual status code is: {actual_status_code}'
    context.logger.info(f'BODY: {context.response.json()}\n\n')


@then('User should be able to see some data in totals')
def step_impl(context):
    totals = context.response.json()['totals']
    assert totals is not None
    new_total = {item['label'].lower(): item['value'] for item in totals}
    clicks = new_total['clicks']
    orders = new_total['orders']
    sales = new_total['sales']
    for name, val in {"clicks": clicks, "sales": sales, "orders": orders}.items():
        assert val is not None, f"{name} is None!"


@when("User clicks on TimeFrame dropdown menu and selects 'Between Dates'")
def step_impl(context):
    context.home_page = HomePage(context.driver)
    click_on_element(context, context.home_page.date_preset)
    context.wait.until(ec.element_to_be_clickable(context.home_page.between_dates))
    click_on_element(context, context.home_page.between_dates)


@when("User selects {start_date} on Start Date input")
def step_impl(context, start_date):
    close_beamer(context)
    context.wait.until(ec.element_to_be_clickable(context.home_page.start_date_input))
    click_on_element(context, context.home_page.start_date_input)
    select_date(context, start_date)


@when("User selects {end_date} on End Date input")
def step_impl(context, end_date):
    sleep(0.4)
    click_on_element(context, context.home_page.end_date_input)
    select_date(context, end_date)
    sleep(4)

@when("User clicks Run btn")
def step_impl(context):
    click_on_element(context, context.home_page.run_btn)
    sleep(5)


@then('User should be able to see following results of: "{Clicks}", "{Orders}", "{Sales}", and "{Commissions}"')
def step_impl(context, Clicks, Orders, Sales, Commissions):
    actual_clicks = context.driver.find_element(*context.home_page.clicks_output).text
    actual_orders = context.driver.find_element(*context.home_page.orders_output).text
    actual_sales = context.driver.find_element(*context.home_page.sales_output).text
    actual_commissions = context.driver.find_element(*context.home_page.commissions_output).text

    assert actual_clicks == Clicks, f'Assertion FAILED: actual clicks are: {actual_clicks} >> expected: {Clicks}. Others: {Orders}, {Sales}, {Commissions}'
    assert actual_orders ==  Orders, f'Assertion FAILED: actual orders are: {actual_orders} >> expected: {Orders}'
    assert actual_sales == Sales, f'Assertion FAILED: actual sales are: {actual_sales} >> expected: {Sales}'
    assert actual_commissions == Commissions, f'Assertion FAILED: actual commissions are: {actual_commissions} >> expected: {Commissions}'