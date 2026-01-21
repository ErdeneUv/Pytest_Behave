import json
from pathlib import Path
import os
from time import sleep

from behave import given, when, then
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from tests.utilities.click_on_element import click_on_element
from tests.pages.brands_page import BrandsPage
from tests.utilities.selenium_utilities import check_spinner


@when(u'user clicks on featured brands logo')
def step_impl(context):
    context.brands_page = BrandsPage(context.driver)
    featured_brands_cards = context.brands_page.elements(context.brands_page.featured_brands_card, 15)

    context.actual_urls = []
    count = len(featured_brands_cards)
    for i in range(count):
        featured_brands_cards = context.brands_page.elements(context.brands_page.featured_brands_card)
        featured_brands_cards[i].click()
        context.actual_urls.append(context.driver.current_url)
        context.driver.back()


@then(u'user should land on brand\'s detail page')
def step_impl(context):
    expected_urls = []
    featured_brands_links = context.brands_page.elements(context.brands_page.featured_brands_link)

    count = 0
    for link in featured_brands_links:
        assert link.get_attribute("href") == context.actual_urls[count], f"Assert failed, expected url {link.get_attribute('href')} is not equal to {context.actual_urls[count]}\n\n"
        count += 1


@then(u'user should see featured brands logos')
def step_impl(context):
    imgs = context.brands_page.elements(context.brands_page.featured_brands_img)

    for i, img in enumerate(imgs, start=1):
        assert img.is_displayed(), f"Featured brand #{i} logo is not displayed."
        natural_width = context.driver.execute_script("return arguments[0].naturalWidth;", img)
        assert natural_width > 0, f"Featured brand #{i} logo is not rendered"


@then(u'user should see brands detail')
def step_impl(context):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the full path to the Excel file
    file_path = str(current_dir.replace("steps", "utilities/test_data/AllBird_details.json"))
    context.file_path = Path(file_path)

    with context.file_path.open("r") as file:
        context.content = json.load(file)
    context.expected_earnings = str(context.content.get("earnings"))
    context.expected_cookie_len = str(context.content.get("cookie_len"))
    #print(f"BRanDETAILS: {context.expected_earnings}, {context.expected_cookie_len}\n\n")

    context.actual_earnings = str(context.brands_page.brand_earnings.get_text())
    context.actual_cookie_len = str(context.brands_page.brand_cookie_len.get_text())

    assert context.expected_earnings == context.actual_earnings, F"Brand's Earnings doesn't match."
    assert context.expected_cookie_len == context.actual_cookie_len, F"Brand's Cookie Length doesn't match."



@then(u'user should see Create Homepage Link form')
def step_impl(context):
    assert context.brands_page.landing_page_link_form_title.is_visible(), (
        "Create Homepage Link form is not displayed"
    )


@then(u'user should see Create A Custom Tracking Link form')
def step_impl(context):
    assert context.brands_page.build_link_form_title.is_displayed(), F"Create A Custom Tracking Link form is not displayed"


@then(u'user should see Share Special Promotions form')
def step_impl(context):
    assert context.brands_page.sp_promo_title.is_displayed(), F"Share Special Promo form is not displayed"


@then(u'user should see Share Banners form')
def step_impl(context):
    assert context.brands_page.share_banners_title.is_displayed(), F"Share Banners form is not displayed"


@when(u'user clicks on Category Filter and clicks on Food and Drink')
def step_impl(context):
    context.brands_page = BrandsPage(context.driver)
    check_spinner(context.driver)
    context.brands_page.category_filter.click()
    context.brands_page.category_filter_food.click()


@when(u'user clicks on letter B filter')
def step_impl(context):
    context.brands_page.letter_filter_b.click()


@then('user should see only these brand with these ID')
def step_impl(context):
    expected_brand_names = []
    expected_brand_ids = []

    for row in context.table:
        expected_brand_names.append(row['Brand'])
        expected_brand_ids.append(row['ID'])

    brands_elements = context.brands_page.elements(context.brands_page.search_result_brands)
    actual_brand_names = [brand.text for brand in brands_elements]
    actual_brand_ids = [brand.get_attribute('href').split('/')[-1] for brand in brands_elements]

    context.cat_filter_brand_numb = len(actual_brand_names)

    for actual, expected in zip(actual_brand_names, expected_brand_names):
        assert actual == expected, f"Expected '{expected}', but got '{actual}'"

    for actual, expected in zip(actual_brand_ids, expected_brand_ids):
            assert actual == expected, f"Expected '{expected}', but got '{actual}'"



@then("user should see Clear button on Cat and Letter Filters")
def step_impl(context):
    assert context.brands_page.category_filter_clear.is_displayed, f'Category Filter is not Displayed'

    assert context.brands_page.letter_filter_clear.is_displayed, f'Letter Filter is not Displayed'


@then("user should not see other letters")
def step_impl(context):
    search_results_letter = context.brands_page.elements(context.brands_page.search_result_letters)
    assert 1 == len(search_results_letter), f'Assertion Failed, actual number of letters: {len(search_results_letter)}'
    expected_letter = ['B']
    actual_letter = [letter.text for letter in search_results_letter]
    assert expected_letter == actual_letter, f'Assertion Failed, actual letter: {actual_letter}'

@when("user clicks on Clear button on Cat Filter")
def step_impl(context):
    context.brands_page.category_filter_clear.click()


@then('user should see total number of brands greater than previous results')
def step_impl(context):
    brands_elements = context.brands_page.elements(context.brands_page.search_result_brands)
    actual_brand_names = [brand.text for brand in brands_elements]

    actual_number_of_brands = len(actual_brand_names)

    assert actual_number_of_brands > context.cat_filter_brand_numb, f"actual:  {actual_number_of_brands} brands, cat_filter: {context.cat_filter_brand_numb} brands were expected"


@when('user clicks on Select a Brand and search for "{target_brand}"')
def step_impl(context, target_brand):
    context.brands_page = BrandsPage(context.driver)
    check_spinner(context.driver)
    by_brand = context.brands_page.search_by_brand

    context.brands_page.search_by_brand.click()
    context.brands_page.search_by_brand_input.type(target_brand)
    in_put = context.brands_page.search_by_brand_input_results
    context.brands_page.search_by_brand_input_results.click()


@then("user should see Category and Letter filters got reset and their Clear button are not displayed")
def step_impl(context):
    assert context.brands_page.search_by_brand_clear.is_displayed
    assert not context.brands_page.category_filter_clear.is_displayed()
    assert not context.brands_page.letter_filter_clear.is_displayed()


@then('user should see only "{expected_brand_name}" under letter "{expected_letter}"')
def step_impl(context, expected_brand_name, expected_letter):
    actual_brand_name = context.brands_page.search_result_brands.get_text()
    assert actual_brand_name == expected_brand_name, f"Expected '{expected_brand_name}' but got '{actual_brand_name}'"

    actual_number_of_brands = len(context.brands_page.elements(context.brands_page.search_result_brands))
    assert 1 == actual_number_of_brands, f"Actual number of brands: {actual_number_of_brands}"

    actual_letter = context.brands_page.search_result_letters.get_text()
    assert actual_letter == expected_letter, f"Expected '{expected_letter}' but got '{actual_letter}'"

    actual_number_of_letters = len(context.brands_page.elements(context.brands_page.search_result_letters))
    assert 1 == actual_number_of_letters, f"Actual number of letters: {actual_number_of_letters}"
