import os
from time import sleep
from behave import given, when, then
from selenium.webdriver.support import expected_conditions as ec
from tests.pages.home_page import HomePage
from tests.pages.tools_page import ToolsPage
from tests.utilities.click_on_element import click_on_element
from tests.utilities.selenium_utilities import close_beamer, check_spinner


@given(u'user navigates to build a link tab')
def step_impl(context):
    home_page = HomePage(context.driver)
    context.tools_page = ToolsPage(context.driver)
    home_page.side_menu_navigate('tools')
    close_beamer(context)
    click_on_element(context, context.tools_page.build_tab)



@when('user enters "{supported_brand}" into Destination URL input on build a link tab')
def step_impl(context, supported_brand):
    context.wait.until(ec.presence_of_element_located(context.tools_page.url_input))
    context.brand_url = os.getenv(supported_brand)
    check_spinner(context.driver)
    print(f'Context.BR_URL: {context.brand_url}\n\n')
    context.driver.find_element(*context.tools_page.url_input).send_keys(context.brand_url)
    click_on_element(context.tools_page, context.tools_page.short_url_checkbox)
    context.url = context.brand_url


@when('user clicks on Create Short URL button on Tools Page')
def step_impl(context):
    click_on_element(context.tools_page, context.tools_page.short_url_checkbox)


@then(u'user should see "Your custom link has been created" msg, and custom link, and Build another link btn')
def step_impl(context):
    context.deeplink = context.driver.find_element(*context.tools_page.deeplink_output).get_attribute('value')
    #print(f'Tools_page_deeplink: {context.deeplink}\n\n\n')
    sleep(2)
    context.wait.until(ec.presence_of_element_located(context.tools_page.created_msg))
    assert context.driver.find_element(*context.tools_page.created_msg).is_displayed(), f'msg did not displayed'
    assert context.driver.find_element(*context.tools_page.deeplink_output).is_displayed(), f'link did not displayed'
    assert context.driver.find_element(*context.tools_page.build_another_btn).is_displayed(), f'build another link did not displayed'



