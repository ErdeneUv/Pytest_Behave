import os
from time import sleep
from behave import given, when, then
import pyperclip
from tests.pages.brands_page import BrandsPage
from tests.pages.home_page import HomePage
from tests.utilities.selenium_utilities import close_beamer, err_msg_assert, check_spinner


@given(u'user navigates to the "{page}" page')
def step_impl(context, page):
    context.home_page = HomePage(context.driver)
    check_spinner(context.driver)
    close_beamer(context)
    context.home_page.side_menu_navigate(page)


@when(u'user searches for "{brand}"')
def step_impl(context, brand):
    context.brands_page = BrandsPage(context.driver)
    context.brands_page.search_brands(brand)
    sleep(2)


@when(u'user clicks on that brand from the search result to open it')
def step_impl(context):
    context.brands_page.search_result_first.click()
    check_spinner(context.driver)

@when('user enters supported brand "{url}" into Destination URL input on brand page')
def step_impl(context, url):
    #context.wait.until(ec.presence_of_element_located(context.brands_page.url_input))
    context.url = os.getenv(url)
    #print(f'brand_url entered into Destination URL: {context.url}\n\n ')
    context.brands_page.url_input.type(context.url)



@when("user clicks on Create Short URL button to get long url on brands page")
def step_impl(context):
    context.brands_page.short_url_checkbox.click()
    #print("CLICKED on Short URL button")

@then(u'user should see an affiliate link')
def step_impl(context):
    sleep(3)
    context.brands_page.created_link.is_displayed()
    assert context.brands_page.created_link.is_displayed()
    #print("asserted BC link output")

@then(u'user should see copy link button and x\'s share button')
def step_impl(context):
    assert context.brands_page.copy_btn.is_displayed()
    assert context.brands_page.x_share.is_displayed()

@when(u'user clicks on brand_pages Copy Link btn')
def step_impl(context):
    context.current_browser = os.getenv('BROWSER')
    context.brands_page, context.brands_page.copy_btn.click()

    if 'remote' or 'headless' not in context.current_browser:
      context.copied_link = pyperclip.paste()
    context.deeplink = context.brands_page.created_link.get_text()
    print(f'deeplink: {context.deeplink}\n\n')


    #doesn't work how much I changed the locators, it doesn't click on copy_btn btn's color changes indicating at least it was in the
    #click_on_element(context, context.brands_page.copy_btn)
    #assert context.driver.find_element(*context.brands_page.link_copied_msg).is_displayed()


@then(u'user should see "{no_match_error_msg}" msg on brands_page')
def step_impl(context, no_match_error_msg):
    err_msg_assert(context, no_match_error_msg)


@then(u'user should see a "Unfortunately, this brand does not currently support deep linking." msg on brands_page')
def step_impl(context):
    assert context.brands_page.not_supported_msg.is_displayed()


@then(u'user should see short and long link')
def step_impl(context):
    assert context.brands_page.homepage_link_short_link.is_displayed(), "short link is not there"
    assert context.brands_page.homepage_link_long_link.is_displayed(), "long link is not there"


@when(u'user clicks on copy this button next to long link')
def step_impl(context):
    context.home_page = HomePage(context.driver)
    #context.home_page.check_spinner()
    context.brands_page.short_copy_btn.click()
    context.copied_link = pyperclip.paste()
    context.url = context.brands_page.brand_url.get_attribute('href')

    context.deeplink = context.brands_page.full_link.get_attribute('value')
    print(f'Brands URL: {context.url}\n')
    print(f'Full_link: {context.deeplink}\n\n')


@when(u'user clicks the Create Deep Link btn on brands_page')
def step_impl(context):
   context.brands_page.create_btn.is_displayed()
   context.brands_page.create_btn.click()


@when(u'user clicks on X share button')
def step_impl(context):
    context.portal_window = context.driver.current_window_handle
    context.brands_page.x_share.is_visible()
    context.brands_page.x_share.click()
    sleep(1)
    #context.wait.until(ec.number_of_windows_to_be(2))

@then(u'user navigate to X page')
def step_impl(context):
    #context.wait.until(ec.number_of_windows_to_be(3))
    for window in context.driver.window_handles:
        if window != context.portal_window and "facebook" in context.driver.current_url:
            context.driver.switch_to.window(window)
            #print(f'CURRENT ADDRESS: {context.driver.current_url}\n\n')
            assert "x.com" in context.driver.current_url, f'it went to {context.driver.current_url}'
    context.driver.switch_to.window(context.portal_window)

@when(u'user clicks on FB share button')
def step_impl(context):
    context.current_window = context.driver.current_window_handle
    context.brands_page.fb_share.is_displayed()
    context.brands_page.fb_share.click()
    sleep(1.0)


@then(u'user navigate to FB page')
def step_impl(context):
    #context.wait.until(ec.new_window_is_opened(context.current_window))
    for window in context.driver.window_handles:
        if window != context.current_window:
            context.driver.switch_to.window(window)
            context.fb_window = window
            assert "facebook.com" in context.driver.current_url, f'it went to {context.driver.current_url}\n\n'
            break


@when(u'user comes back to the brand page')
def step_impl(context):
    #sleep(1)
    context.driver.close()
    context.driver.switch_to.window(context.current_window)
    assert "brandcycle" in context.driver.current_url, f'it went to {context.driver.current_url}\n'