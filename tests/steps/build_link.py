import os
from time import sleep
from behave import given, when, then
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
import pyperclip
from selenium.webdriver.support.wait import WebDriverWait

from tests.pages.brands_page import BrandsPage
from tests.pages.home_page import HomePage
from tests.pages.login_page import LoginPage
from tests.utilities.click_on_element import click_on_element
from tests.utilities.final_url import fin_url
from tests.utilities.selenium_utilities import close_beamer, check_spinner, check_loading_dots
from tests.utilities.url_assertion import url_assertion


@given(u'user logs in as a "{user}"')
def step_impl(context, user):
    context.login_page = LoginPage(context.driver)
    context.wait.until(ec.presence_of_element_located(context.login_page.username_input))

    context.login_page.login_by_role_click(user)
    context.home_page = HomePage(context.driver)
    env_url = os.getenv('BASE_URL')
    close_beamer(context)
    context.wait.until(ec.invisibility_of_element_located(context.home_page.spinner))
    assert env_url in context.driver.current_url, f"not on {env_url}, current_url: {context.driver.current_url}\n\n\n"


@then(u'user should see snapshot report title')
def step_impl(context):
    #check_spinner(context.driver)
    WebDriverWait(context.driver, 5).until(ec.presence_of_element_located(context.home_page.snapshot_title))
    assert context.driver.find_element(*context.home_page.snapshot_title).is_displayed(), f"Snapshot report is not Displayed"


@then(u'user should see build a link form title')
def step_impl(context):
    assert context.driver.find_element(*context.home_page.build_form_title).is_displayed(), f"Build a Link form in HomePage is not Displayed"


@then(u'user should see Featured Announcements')
def step_impl(context):
    close_beamer(context)
    assert context.driver.find_element(*context.home_page.announcements_head_title).is_displayed(), f"Featured Announcement title is not Displayed"

    ann_cards = context.driver.find_elements(*context.home_page.announcements_card)
    for i, element in enumerate(ann_cards, start=1):
        assert element.is_displayed(), f"Announcements Cards #{i} is not displayed"

    ann_titles = context.driver.find_elements(*context.home_page.announcements_title)
    for i, element in enumerate(ann_titles, start=1):
        assert element.is_displayed(), f"Announcements Titles #{i} is not displayed"

    ann_img = context.driver.find_elements(*context.home_page.announcements_img)
    for i, element in enumerate(ann_img, start=1):
        assert element.is_displayed(), f"Announcements Image #{i} is not displayed"
        natural_width = context.driver.execute_script(
            "return arguments[0].naturalWidth;", element
        )
        assert natural_width > 0, f"Image failed to load, natural width: {natural_width}\n"

    ann_body = context.driver.find_elements(*context.home_page.announcements_body)
    for i, element in enumerate(ann_body, start=1):
        assert element.is_displayed(), f"Announcement Body #{i} is not displayed"


@then(u'user should see Socials')
def step_impl(context):
    assert context.driver.find_element(*context.home_page.social_head_title).is_displayed()
    assert context.driver.find_element(*context.home_page.social_instagram_icon).is_displayed()
    assert context.driver.find_element(*context.home_page.social_fb_icon).is_displayed()
    assert context.driver.find_element(*context.home_page.social_x_icon).is_displayed()


@then(u'user should see Blogs')
def step_impl(context):
    assert context.driver.find_element(*context.home_page.blog_head_title).is_displayed()

    blog_titles = context.driver.find_elements(*context.home_page.blog_head_title)
    for i, element in enumerate(blog_titles, start=1):
        assert element.is_displayed(), f"Blog Titles #{i} is not displayed"

    blog_dates = context.driver.find_elements(*context.home_page.blog_date)
    for i, element in enumerate(blog_dates, start=1):
        assert element.is_displayed(), f"Blog date #{i} is not displayed"

    blog_imgs = context.driver.find_elements(*context.home_page.blog_img)
    for i, element in enumerate(blog_imgs, start=1):
        assert element.is_displayed(), f"Blog img #{i} is not displayed"

    blog_body = context.driver.find_elements(*context.home_page.blog_body)
    for i, element in enumerate(blog_body, start=1):
        assert element.is_displayed(), f"Blog body #{i} is not displayed"

    read_more = context.driver.find_elements(*context.home_page.blog_read_more)
    for i, element in enumerate(read_more, start=1):
        assert element.is_displayed(), f"Blog read more #{i} is not displayed"


@then(u'user should see bottom elements')
def step_impl(context):
    assert context.driver.find_element(*context.home_page.footer_social_insta), f"Insta Icon in the footer is missing"
    assert context.driver.find_element(*context.home_page.footer_social_fb), f"FB Icon in the footer is missing"
    assert context.driver.find_element(*context.home_page.footer_social_x), f"X Icon in the footer is missing"
    assert context.driver.find_element(*context.home_page.footer_copy_right), f"Copy right in the footer is missing"


@when(u'user enters supported brand "{url}" into Destination URL input')
def step_impl(context, url):
    context.url = os.getenv(url)
    print(f'Target Link: {context.url}\n\n')
    #sleep(1)
    context.home_page.build_a_link(context.url)

   #this is for url_sanitization feature
@when(u'user enters supported "{url}" into Destination URL input')
def step_impl(context, url):

    print(f'Target Link: {url}\n\n')
    context.home_page = HomePage(context.driver)
    #sleep(1)
    context.url = url
    context.home_page.build_a_link(context.url)


@when("user clicks on Create Short URL button to get long url")
def step_impl(context):
    action = ActionChains(context.driver)
    short_url_btn = context.driver.find_element(*context.home_page.short_url_btn)
    action.click(short_url_btn).perform()
    #click_on_element(context, context.home_page.short_url_btn)


@when(u'user clicks the Create Deep Link btn')
def step_impl(context):
    context.home_page = HomePage(context.driver)
    click_on_element(context, context.home_page.create_dlink_btn)
    check_loading_dots(context.driver)

@then(u'the user should get a short or long brandcycle link')
def step_impl(context):
    context.wait.until(ec.invisibility_of_element_located(context.home_page.loading_dots))
    #due to headless browser or headless container in pipelines, test automation gets the BC link from link output field in context.deeplink for remote drivers or use pyperclip for headless browsers.
    context.deeplink = context.driver.find_element(*context.home_page.deeplink_output).get_attribute('value')
    print(f'BC link: {context.deeplink}\n\n')
    assert context.deeplink != '', f'Did not get a short or long brandcycle link'


@when(u'user clicks on Copy Link btn')
def step_impl(context):
    context.current_browser = os.getenv('BROWSER')
    click_on_element(context, context.home_page.copy_link_btn)
    if 'remote' not in context.current_browser and 'headless' not in context.current_browser:
        context.copied_link = pyperclip.paste()

    #if browser is in tools page it got BC link from deeplink output field's value attribute
    if context.__contains__('tools_page'):
        context.deeplink = context.driver.find_element(*context.tools_page.deeplink_output).get_attribute('value')
    sleep(0.3)

    if context.__contains__('tools_page'):
        assert context.driver.find_element(*context.tools_page.link_copied).is_displayed(), f'Link Copied msg didnt show up'
    else:
        assert context.driver.find_element(*context.home_page.link_copied).is_displayed(), f'Link Copied msg didnt show up'


@when(u'opens the link')
def step_impl(context):
    if 'remote' in context.current_browser:
        context.headless_current_url = fin_url(context.deeplink, context.url)

    elif 'headless' in context.current_browser:
        context.headless_current_url = fin_url(context.deeplink, context.url)

    else:
        context.current_url = fin_url(context.copied_link, context.url)

    #print(f'context.url: {context.url}\n')
    #print(f'remote, headless opens the link: {context.headless_current_url}\n\n')
    #print(f'normal: {context.current_url}\n\n\n')


@then(u'the user should see the brand page that was used as Destination url.')
def step_impl(context):
    #current_url = context.driver.current_url
    #Due to hdless browser limitation, it has two different implementation of checking if BC link lands on the page url it produced the link from. Also, the BC links got a few redirections and final url got changed, if first assertion fails, it splits the url by '?' and compare first half.
    if any(keyword in context.current_browser for keyword in ['remote', 'headless']):
        print(f'Target_URL: {context.url}')
        print(f'BC_URL: {context.headless_current_url}\n\n')
        url_assertion(context.url, context.headless_current_url)
    else:
        url_assertion(context.url, context.current_url)
    context.copied_link = ""


@when(u'user enters "{inactive_brand_url}" into Destination URL input')
def step_impl(context, inactive_brand_url):
    context.brand_url = os.getenv(inactive_brand_url)
    context.home_page = HomePage(context.driver)
    context.home_page.build_a_link(context.brand_url)


@then(u'user should see "{msg}" msg')
def step_impl(context, msg):
    context.home_page = HomePage(context.driver)
    context.home_page.error_msg_check(msg)


@then(u'user should not see the brand in BrandPage')
def step_impl(context):
    context.brands_page = BrandsPage(context.driver)
    assert context.brands_page.brand_doesnt_exist(context, context.brand_url)


@when(u'user enters "{blacklisted_brand_url}" into Destination URL input for a brand they are blacklisted for')
def step_impl(context, blacklisted_brand_url):
    context.home_page = HomePage(context.driver)
    context.brand_url = os.getenv(blacklisted_brand_url)
    context.home_page.build_a_link(context.brand_url)


@then(u'user should see the "{empty}" error message')
def step_impl(context, empty):
    assert context.driver.find_element(*context.home_page.empty_error_msg) is not None


@when(u'user enters unavailable brand url')
def step_impl(context):
    context.home_page = HomePage(context.driver)
    context.driver.find_element(*context.home_page.url_input).send_keys(context.config.userdata['unavailable_brand'])


@when(u'user enters unauthorized url')
def step_impl(context):
    context.home_page = HomePage(context.driver)
    context.driver.find_element(*context.home_page.url_input).send_keys(context.config.userdata['unauthorized_url'])


@when(u'user enters private brand for deep link')
def step_impl(context):
    context.home_page = HomePage(context.driver)
    context.driver.find_element(*context.home_page.url_input).send_keys(context.config.userdata['private_brand'])


@then(u'user should see PRIVATE BRANDS error message')
def step_impl(context):
    assert context.driver.find_element(*context.home_page.url_error_msg)


@then(u'user should see "THE BRANDS HAS NOT AUTHORIZED" error message')
def step_impl(context):
    assert context.driver.find_element(*context.home_page.url_error_msg).is_displayed()


@then(u'user sees "see all other brand" link')
def step_impl(context):
    assert context.driver.find_element(*context.home_page.other_brands_link).is_displayed()


@when(u'user clicks the Create Deep Link btn on homepage')
def step_impl(context):
    context.home_page = HomePage(context.driver)

    click_on_element(context, context.home_page.create_dlink_btn)
    context.driver.execute_script("arguments[0].click();", context.driver.find_element(*context.home_page.create_dlink_btn))
    click_on_element(context, context.home_page.short_url_btn)