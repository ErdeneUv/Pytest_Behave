from time import sleep
from behave import *
from tests.pages.home_page import HomePage
from tests.pages.reports_page import ReportsPage
from tests.utilities.api_utilities import get_subusers, get_engaged_brands, get_lpr
from tests.utilities.click_on_element import click_on_element
from tests.utilities.selenium_utilities import select_date, close_beamer, month_counter


@when('user enters "{start_date}" for star date and "{end_date}" for end date')
def step_impl(context, start_date, end_date):
    context.report_page = ReportsPage(context.driver)
    close_beamer(context)
    context.report_page.start_date_lpr.click()
    select_date(context, start_date)
    #sleep(0.5)
    context.report_page.end_date_lpr.click()
    select_date(context, end_date)


@when('user filters for "{brand}"')
def step_impl(context, brand):
    #sleep(2.5)
    context.report_page.brand_filter_dropdown.click()
    context.report_page.brand_filter_input.click()
    context.report_page.brand_filter_input.type(brand)
    context.report_page.brand_filter_first_option.click()

@when("user sort by Sales")
def step_impl(context):
    context.report_page.sales_header.click()
    #sleep(2.5)

@then('user will see "{sales}", "{clicks}", "{orders}" matching')
def step_impl(context, sales, clicks, orders):
    actual_sales = context.report_page.sales_first.get_text()
    actual_clicks = context.report_page.clicks_first.get_text()
    actual_orders = context.report_page.orders_first.get_text()

    assert actual_sales == sales, f"assertion failed on sales, actual sales: {actual_sales}\nexpected sales: {sales}\nactual sales: {actual_sales}\nclicks: {actual_clicks}"
    assert actual_clicks == clicks, f"assertion failed on clicks, actual clicks: {actual_clicks}"
    assert actual_orders == orders, f"assertion failed on orders, actual orders: {actual_orders}"


@when('user clicks on "{clicks}" header to sort by it')
def step_impl(context, clicks):
    context.report_page.lpr_sort(clicks)


@then('user will see "{expected_clicks}" on first row\'s clicks')
def step_impl(context, expected_clicks):
    actual_clicks = context.report_page.clicks_first.get_text()
    assert actual_clicks == expected_clicks, f"assertion failed on clicks numbers, actual clicks: {actual_clicks}\nexpected clicks: {expected_clicks}\n\n"


@then('user will see "{expected_payout}" on first row\'s payout')
def step_impl(context, expected_payout):
    actual_payout = context.report_page.payout_first.get_text()
    assert actual_payout == expected_payout, f"assertion failed on payout, actual payout: {actual_payout}\nexpected payout: {expected_payout}\n\n"

@when('user clicks on "3M" date preset')
def step_impl(context):
    context.report_page = ReportsPage(context.driver)
    context.report_page.three_m.click()
    context.report_page.link_pag.click()
    link_number = str(context.report_page.link_pag.get_text())
    context.three_m_link_number = int(link_number.split()[-2])
    close_beamer(context)

@then("user should see date for today in end date and 3 months back in start date")
def step_impl(context):
    start_date = context.report_page.start_date_lpr.get_attribute("value")
    end_date = context.report_page.end_date_lpr.get_attribute("value")
    month_counted = month_counter(start_date, end_date)
    assert month_counted == 3, f'assertion failed on 3 month, actual month: {month_counted}\n\n'


@then("user should see date for today in end date and 1 month back in start date")
def step_impl(context):
    start_date = context.report_page.start_date_lpr.get_attribute("value")
    end_date = context.report_page.end_date_lpr.get_attribute('value')
    month_counted = month_counter(start_date, end_date)
    assert month_counted == 1, f'assertion failed on 3 month, actual month: {month_counted}\n\n'


@then("user should see less number of links and pages")
def step_impl(context):
    assert context.three_m_link_number > context.one_m_link_number, f"link number assertion failed, 3m link number: {context.three_m_link_number}, 1m link number: {context.one_m_link_number}\n\n\n"

@when("user logs out")
def step_impl(context):
    home_page = HomePage(context.driver)
    click_on_element(context, home_page.account_dashboard_btn)
    click_on_element(context, home_page.logout)

@when('user clicks on User Filter and choose "{user_one}", "{user_two}", and "{user_three}')
def step_impl(context, user_one, user_two, user_three):
    context.report_page.user_filter_dropdown.click()
    context.report_page.user_filter_input.click()
    context.report_page.user_filter_input.type(user_one)
    context.report_page.user_filter_first_option.click()
    context.report_page.user_filter_input.clear_all()
    context.report_page.user_filter_input.type(user_two)
    context.report_page.user_filter_first_option.click()
    context.report_page.user_filter_input.clear_all()
    context.report_page.user_filter_input.type(user_three)
    context.report_page.user_filter_first_option.click()

@then('user would see "{expected_links}" links and total of "{expected_pages}" pages')
def step_impl(context, expected_links, expected_pages):
    context.report_page.link_pag.click()
    link_number = context.report_page.link_pag.get_text()
    actual_links = link_number.split()[-2]

    actual_pages = context.report_page.page_pag.get_text()
    actual_pages = actual_pages.removeprefix("of ")
    context.expected_links = expected_links

    assert actual_pages == expected_pages, f"on pages, actual pages: {actual_pages}\nexpected pages: {expected_pages}\n\n"
    assert actual_links == expected_links, f"on links, actual links: {actual_links}\nexpected links: {expected_links}\n\n"


@when("user clicks on clear filters")
def step_impl(context):
    context.report_page.clear_btn.click()
    sleep(0.5)


@then('user would see more than "13" links')
def step_impl(context):
    link_number = context.report_page.link_pag.get_text()
    actual_links = link_number.split()[-2]
    assert actual_links > context.expected_links, f"Assertion failed on link numbers, actual links: {actual_links}\nexpected: {context.expected_links}\n\n"


@when('user clicks on "1M" date preset')
def step_impl(context):
    context.report_page.one_m.click()
    context.report_page.link_pag.click()
    link_number = str(context.report_page.link_pag.get_text())
    context.one_m_link_number = int(link_number.split()[-2])
    close_beamer(context)


@when('user sends a request to "subusers" as a "{user}"')
def step_impl(context, user):
    context.resp_sub = get_subusers(user)
    assert context.resp_sub.status_code == 200, f'request to subusers did not got status code 200, instead: {context.resp_sub.status_code}'


@then('user will receive status code "{status_code}" and subusers\' uid')
def step_impl(context, status_code):
    actual_status_code = context.resp_sub.status_code
    assert str(actual_status_code) == status_code, f'on subusers status code, actual status code: {actual_status_code}\nresp: {context.resp_sub.json()}\n\n\n'


@when('user sends a request to "brands-engaged" for userID "{user_id}"')
def step_impl(context, user_id):
    context.resp = get_engaged_brands(user_id)


@then('user receives a status code "{expected_status_code}" and engaged brand\'s ids')
def step_impl(context, expected_status_code):
    actual_status_code = str(context.resp.status_code)
    assert actual_status_code == expected_status_code, f'on status code, actual status code: {actual_status_code}\n\n'

@when(
    'user sends a request to "link-performance" as a "{user}" for userID "{user_id}", brandID "{brand_id}", createdAfter "{period_start}", createdBefore "{period_end}", sort "{sort}", direction "{direction}"')
def step_impl(context, user, user_id, brand_id, period_start, period_end, sort, direction):
    context.resp = get_lpr(user, user_id, brand_id, period_start, period_end, sort, direction)


@then('user will get status code of "{200}"')
def step_impl(context, expected_status_code):
    actual_status_code = context.resp.status_code
    assert str(actual_status_code) == expected_status_code, f'on status code, actual status code: {actual_status_code}\nresp: {context.resp.json()}'

@then('user will get sales: "{sales}", payout: "{payout}" clicks: "{clicks}", orders: "{orders}", conversionRate: "{conversion_rate}"')
def step_impl(context, sales, payout, clicks, orders, conversion_rate):
    data = context.resp.json()
    actual_sales = data["data"][0]["sales"]
    actual_payout = data["data"][0]["payout"]
    actual_clicks = data["data"][0]["clicks"]
    actual_orders = data["data"][0]["orders"]
    actual_conversion_rate = data["data"][0]["conversionRate"]

    assert actual_sales == float(sales), f'on sales, actual sales: {actual_sales}\n\n\n'
    assert actual_payout == float(payout), f'on payout, actual payout: {actual_payout}\n\n\n'
    assert actual_clicks == float(clicks), f'on clicks, actual clicks: {actual_clicks}\n\n\n'
    assert actual_orders == float(orders), f'on orders, actual orders: {actual_orders}\n\n\n'
    assert actual_conversion_rate == float(conversion_rate), f'on conversion_rate, actual conversion_rate: {actual_conversion_rate}\n\n\n'


@when(
    'user sends a request to "link-performance" as a "{user}" for userID "{user_id}", sort "{sort}", direction "{direction}", periodStart "{period_start}", periodEnd "{period_end}"')
def step_impl(context, user, user_id, sort, direction, period_start, period_end):
    context.resp = get_lpr(user, user_id= user_id, sort= sort, direction= direction, period_start= period_start, period_end= period_end)


@then('user will get totalItems: "{total_item}", totalPages: "{total_pages}" in meta of payload')
def step_impl(context, total_item, total_pages):
    data = context.resp.json()
    actual_total_items = data["meta"]["totalItems"]
    actual_total_pages = data["meta"]["totalPages"]

    assert actual_total_items == int(total_item), f'on total items, actual total items: {actual_total_items}, {type(actual_total_items)}\n\n\n'
    assert actual_total_pages == int(total_pages), f'on total pages, actual total pages: {actual_total_pages}\n\n\n'

