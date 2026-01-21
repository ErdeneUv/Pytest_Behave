from behave import given, when, then
from tests.pages.login_page import LoginPage
from tests.utilities.click_on_element import click_on_element
from selenium.webdriver.support import expected_conditions as ec

@given(u'user clicks on Reset password here button')
def step_impl(context):
    context.login_page = LoginPage(context.driver)
    click_on_element(context, context.login_page.reset_password)


@given(u'user lands on password reset page')
def step_impl(context):
    context.wait.until(ec.presence_of_element_located(context.login_page.reset_pwd_msg))

    assert context.driver.find_element(*context.login_page.reset_pwd_msg).is_displayed


@when(u'user enters "{username}" and clicks on send button')
def step_impl(context, username):
    context.driver.find_element(*context.login_page.username_input).send_keys(username)
    context.wait.until(ec.element_to_be_clickable(context.login_page.send_btn))

    click_on_element(context, context.login_page.send_btn)


@then(u'user sees message')
def step_impl(context):
    context.wait.until(ec.presence_of_element_located(context.login_page.reset_pwd_post_msg))

    assert context.driver.find_element(*context.login_page.reset_pwd_post_msg).is_displayed


@when(u'user clicks on Back to login button')
def step_impl(context):
    click_on_element(context, context.login_page.back_to_login)


@then(u'user sees login page')
def step_impl(context):
    context.wait.until(ec.presence_of_element_located(context.login_page.welcome_msg))
    assert context.driver.find_element(*context.login_page.welcome_msg).is_displayed
