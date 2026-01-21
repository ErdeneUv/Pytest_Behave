import os
from time import sleep
from behave import  when, then
import pyperclip
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from tests.pages.promo_page import PromoPage
from tests.utilities.api_utilities import get_dealID, get_promo_link
from tests.utilities.click_on_element import click_on_element
from pathlib import Path
from tests.utilities.selenium_utilities import close_beamer, check_spinner, _resolve_download_dir_from_driver, \
    current_time_marker, wait_for_new_file


@when(u'user searches for "{keyword}" keyword on promo page')
def step_impl(context, keyword):
    context.promo_page = PromoPage(context.driver)
    context.driver.find_element(*context.promo_page.search_input).send_keys(keyword)
    #context.url = 'www.'+ 'whitehouseblackmarket' + '.com'

@when('user filters by "{brand}" brand on promo page')
def step_impl(context, brand):
    sleep(1)

    brands_dropdown = context.driver.find_element(*context.promo_page.brands_dropdown)
    context.action.move_to_element(brands_dropdown).click(brands_dropdown).perform()

    brand_filter_input = context.driver.find_element(*context.promo_page.brands_filter_input)
    context.action.move_to_element(brand_filter_input).click(brand_filter_input).perform()

    brand_filter_input.send_keys(brand)

    brand_filter_result = context.driver.find_element(*context.promo_page.brands_filter_result)
    context.action.move_to_element(brand_filter_result).click(brand_filter_result).perform()

    context.url = 'https://www.wineaccess.com'
    #brand's home page is hard coded here this is used in fin_url()


@when("user sort by End Date and Oldest")
def step_impl(context):
    sort_dropdown = context.driver.find_element(*context.promo_page.sort_dropdown)
    context.action.move_to_element(sort_dropdown).click(sort_dropdown).perform()

    sort_end = context.driver.find_element(*context.promo_page.sort_end_date)
    context.action.move_to_element(sort_end).click(sort_end).perform()

    order_dropdown = context.driver.find_element(*context.promo_page.order_dropdown)
    context.action.move_to_element(order_dropdown).click(order_dropdown).perform()

    order_oldest = context.driver.find_element(*context.promo_page.order_oldest)
    context.action.move_to_element(order_oldest).click(order_oldest).perform()

    filter = context.driver.find_element(*context.promo_page.filter_btn)
    context.action.move_to_element(filter).click(filter).perform()


@then(u'user should see the brand name on the first tile')
def step_impl(context):
    context.wait.until(ec.presence_of_element_located(context.promo_page.first_brand_title))
    assert context.driver.find_element(*context.promo_page.first_brand_title).is_displayed()


@when(u'user clicks on "Create Link" btn on the first tile')
def step_impl(context):
    check_spinner(context.driver)
    click_on_element(context, context.promo_page.first_tile_generate_btn)
    context.wait.until(
        lambda d: ((el := context.driver.find_element(*context.promo_page.created_link)) and
                   (t := (el.text or el.get_attribute("textContent") or "").strip()) and
                   t is not None)
    )
    sleep(1)

@then(u'user should be able to see a created deep link, copy link btn, FB and X share button')
def step_impl(context):
    assert context.driver.find_element(*context.promo_page.created_link).is_displayed()
    assert context.driver.find_element(*context.promo_page.link_generated_btn).is_displayed()
    assert context.driver.find_element(*context.promo_page.fb_share_btn).is_displayed()
    assert context.driver.find_element(*context.promo_page.x_share_btn).is_displayed()


@when(u'user clicks on Copy Link btn on promo page')
def step_impl(context):
    context.wait.until(ec.element_to_be_clickable(context.promo_page.copy_link_btn))
    click_on_element(context, context.promo_page.copy_link_btn)

    context.copied_link = pyperclip.paste()
    context.current_browser= os.getenv('BROWSER')
    if 'headless' or 'remote' in context.current_browser:
        context.deeplink = context.driver.find_element(*context.promo_page.created_link).text
    else:
        context.deeplink = context.copied_link

    context.url = 'https://www.wineaccess.com'
    #print(f'COPIED LINK: {context.deeplink}\n\n\n')

@when("user clicks on Export All button")
def step_impl(context):
    export_btn = context.driver.find_element(*context.promo_page.export_btn)
    context._download_dir = _resolve_download_dir_from_driver(context)
    context._pre_click_marker = current_time_marker(context._download_dir)
    context.action.move_to_element(export_btn).click(export_btn).perform()


@then('user sees downloaded file with name containing "{expected_file_name}"')
def step_impl(context, expected_file_name):
    download_dir: Path = getattr(context, "_download_dir", _resolve_download_dir_from_driver(context))
    marker = getattr(context, "_pre_click_marker", None)
    assert marker, "Missing pre-click time marker; call the @when step first."

    new_file = wait_for_new_file(download_dir, before_timestamp=marker, timeout=360)
    # Assert name contains the substring (case-insensitive)
    print(f'file name: {new_file.name}\n\n\n')
    assert expected_file_name in new_file.name.lower(), \
        f"Expected '{expected_file_name}' in filename, got '{new_file.name}'"


@when('user sends a request to portal with payloads of keywords : "{keywords}", brandTitle : "{brand_title}"')
def step_impl(context, keywords, brand_title):
    context.deal_resp = get_dealID(keywords, brand_title)
    #print(f'deal_resp: {context.deal_resp}, status_code: {context.deal_resp.status_code}\n\n\n')
    brand_title = brand_title.replace(' ', '') if ' ' in brand_title else brand_title
    context.url = f'https://www.{brand_title.lower()}.com'


@then('user will receive a status code "200" and response with dealID of "Wine Access"')
def step_impl(context):
    assert context.deal_resp.status_code == 200, f'get_dealID() failed, status code: {context.deal_resp.status_code}\n'
    data = context.deal_resp.json()
    context.deal_id = data['specialPromotions'][0]['dealID']
    assert context.deal_id is not None, f'Failed to get dealID, dealID: {context.deal_id}\n'


@when("user sends a request to get promo link")
def step_impl(context):
    context.promo_resp = get_promo_link(context.deal_id)
    #print(f'promo_resp: {context.promo_resp}\nstatus_code: {context.promo_resp.status_code}\n\n\n')


@then('user will receive status code "200" and promo link')
def step_impl(context):
    assert context.promo_resp.status_code == 200, f"Failed, get_promo_link() failed, status code: {context.promo_resp.status_code}\n"
    context.promo_link = context.promo_resp.json()
    #print(f'promo_link: {context.promo_link}\n\n')
    assert context.promo_link is not None

    context.long_url = context.promo_link


@when('user sends a request to portal with payloads of brandTitle : "{brand}", sortBy : "{sort_by}", orderBy : "{order_by}"')
def step_impl(context, brand, sort_by, order_by):
    keywords = ''
    context.deal_resp = get_dealID(brand_title=brand, sort_by = sort_by, order_by = order_by)
    #print(f'deal_resp: {context.deal_resp}, status_code: {context.deal_resp.status_code}\n\n\n')
    context.url = f'https://www.{brand.lower()}.com'


@then('user will receive a status code "200", response with dealID of "{brand}", description of "{expected_desc}"')
def step_impl(context, brand, expected_desc):
    assert context.deal_resp.status_code == 200, f"Failed, get_dealID() failed, status code: {context.deal_resp.status_code}\n"

    data = context.deal_resp.json()

    deal_brand = data['specialPromotions'][0]['title']
    assert deal_brand == brand, f"Assertion Failed, get_dealID() failed, brand: {deal_brand}\n"

    deal_desc = data['specialPromotions'][0]['details']['description']
    assert deal_desc == expected_desc, f"Assertion Failed, get_dealID() failed, description: {deal_desc}\n"

    context.deal_id = data['specialPromotions'][0]['dealID']
