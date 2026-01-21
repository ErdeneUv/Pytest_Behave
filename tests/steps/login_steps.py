import os

from behave import given, when, then
from selenium.webdriver.support import expected_conditions as ec
from tests.pages.home_page import HomePage
from tests.pages.login_page import LoginPage
from tests.utilities.selenium_utilities import check_spinner, close_beamer


@given('user is on Login Page')
def step_impl(context):
    context.login_page = LoginPage(context.driver)


@when('"{user}" enter correct credentials')
def step_impl(context, user):
    context.login_page.login_by_role(user)


@then(u'user logged in successfully and redirected to Main Page')
def step_impl(context):
    context.home_page = HomePage(context.driver)
    #check_spinner(context.driver)
    #close_beamer(context)
    context.wait.until(ec.presence_of_element_located(context.home_page.account_dashboard_btn))

    actual_text = context.driver.find_element(*context.home_page.account_dashboard_btn).text
    expected_text = context.config.userdata['home_page_txt']

    assert expected_text in actual_text, f'Expected {expected_text} to be in {actual_text}'

@when('user enter incorrect "{username}" and "{password}"')
def step_impl(context, username, password):
    username = context.config.userdata[username]
    password = context.config.userdata[password]
    context.login_page.login(username, password)


@then(u'user gets error message')
def step_impl(context):
    context.wait.until(ec.presence_of_element_located(context.login_page.login_error_msg))

    error_msg = context.driver.find_element(*context.login_page.login_error_msg)
    assert error_msg.is_displayed()


