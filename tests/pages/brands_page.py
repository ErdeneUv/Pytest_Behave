import os
from time import sleep

from parse_type.parse import search
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from tests.pages.base_page import BasePage
from tests.utilities.get_br_name import get_br_name
from tests.utilities.click_on_element import click_on_element
from tests.utilities.selenium_utilities import check_spinner


class BrandsPage(BasePage):
    # --- Filters ---
    CATEGORY_FILTER = (By.XPATH, "//button[@id='categories']")
    CATEGORY_FILTER_FOOD = (By.XPATH, "//li[contains(text(), 'Food')]")
    CATEGORY_FILTER_CLEAR = (By.XPATH, "(//button[@class='baseDropdown__labelButton'])[1]")
    LETTER_FILTER_ALL = (By.XPATH, "//button[.='All']")
    LETTER_FILTER_B = (By.XPATH, "//button[.='B']")
    LETTER_FILTER_CLEAR = (By.XPATH, "//button[@class='brandsSelector__letterFilterLabelButton']")

    # --- Search ---
    SEARCH_BY_BRAND = (By.XPATH, "//button[@id='retailers']")
    SEARCH_BY_BRAND_INPUT = (By.XPATH, "//input[@class='baseDropdown__menuSearchInput']")
    SEARCH_BY_BRAND_RESULT = (By.CLASS_NAME, "baseDropdown__menuListOption ")
    SEARCH_BY_BRAND_NO_RESULT = (By.XPATH, "//li[.='No results found']")
    SEARCH_BY_BRAND_CLEAR = (By.XPATH, "(//button[@class='baseDropdown__labelButton'])[2]")

    # --- Results ---
    SEARCH_RESULT_LETTERS = (By.XPATH, "//div[@class='brandsCollection__letterGroup']/h2")
    SEARCH_RESULT_BRANDS = (By.XPATH, "//li[@class='brandsCollection__letterGroupListItem']/a")
    SEARCH_RESULT_FIRST = (By.XPATH, "//a[@class='brandsCollection__letterGroupListItemLink']")
    SEARCH_RESULT_LETTER_A = (By.XPATH, "//h2[.='A']")
    SEARCH_RESULT_LETTER_B = (By.XPATH, "//h2[.='B']")
    SEARCH_RESULT_BEAN_BOX = (By.XPATH, "//a[.='Bean Box']")
    BRAND_URL = (By.CLASS_NAME, "brandDetailsHeader__url")
    CAT_FILTER = (By.XPATH, "//button[@id='categories']")
    SEARCH_BY_BRAND_INPUT_RESULTS = (By.XPATH, "//li[@class='baseDropdown__menuListOption ']")

    # --- Create link form ---
    BUILD_LINK_FORM_TITLE = (By.XPATH, "//h2[@class='createDeepLink__title']")
    LANDING_PAGE_LINK_FORM_TITLE = (By.XPATH, "//h2[@class='createHomepageLink__title']")
    GENERATE_HOMEPAGE_LINK_BTN = (By.CLASS_NAME, "c-hjfmDJ-ibMBskE-css")
    URL_INPUT = (By.XPATH, "//input[@type='url']")
    SHORT_URL_BTN = (By.XPATH, "//button[@id='deepLinking']")
    CREATE_BTN = (By.XPATH, "(//span[.='Create Link'])[1]")
    CREATE_ANOTHER_BTN = (By.XPATH, "(//span[.='Create Another Link'])[1]")
    AFF_TRACKING_INPUT = (By.XPATH, "//input[@type='text']")
    SHORT_URL_CHECKBOX = (By.XPATH, "//input[@id='deepLinking']")
    CREATE_LINK_BTN = (By.XPATH, '//button[@data-event="homepage-create-link-btn"]')
    NO_OPTION = (By.CLASS_NAME, "css-1wlit7h-NoOptionsMessage")
    LOADING_DOTS = (By.CLASS_NAME, "loadingDots baseButton__loading")

    # --- Created link part ---
    CREATED_LINK = (By.XPATH, "(//button[@class='buttonCopy buttonsCreateCopy__copy'])[1]")
    COPY_BTN = (By.XPATH, "(//span[@class='baseIcon buttonCopy__icon'])[1]")
    FB_SHARE = (By.XPATH, "//button[contains(@class, 'socialShare__button--facebook')]")
    X_SHARE = (By.XPATH, "//button[contains(@class, 'socialShare__button--twitter')]")
    LINK_COPIED_MSG = (By.XPATH, "//div[.='Link Copied']")
    ERROR_MSG = (By.XPATH, "//div[@role='alert']")
    ERROR_MSG_TEXT = (By.XPATH, "//p[@class='errorMessage__content']")

    # --- Deeplink not enabled ---
    NOT_SUPPORTED_MSG = (By.CSS_SELECTOR, "p[class='errorMessage__content']")
    HOMEPAGE_LINK_SHORT_LINK = (By.XPATH, "(//button[@class='buttonCopy buttonsCopyPrefilled__labelLink'])[1]")
    HOMEPAGE_LINK_LONG_LINK = (By.XPATH, "(//button[@class='buttonCopy buttonsCopyPrefilled__labelLink'])[2]")
    SHORT_COPY_BTN = (By.XPATH, "(//button[contains(@class, 'linkGenFormContent__button--copy')])[1]")
    LONG_COPY_BTN = (By.XPATH, "(//button[contains(@class, 'linkGenFormContent__button--copy')])[2]")

    # --- Brand's details ---
    BRAND_LOGO = (By.XPATH, "//img[@class='baseImage  brandDetailsHeader__logo']")
    BRAND_TITLE = (By.XPATH, "//h1[@class='brandDetailsHeader__title']")
    BRAND_URL = (By.XPATH, "//a[@class='brandDetailsHeader__url']")
    BRAND_EARNINGS = (By.XPATH, "//dd[@class='brandStats__value brandStats__value--earnings']")
    BRAND_COOKIE_LEN = (By.XPATH, "//dd[@class='brandStats__value brandStats__value--cookie']")

    # --- Share special promo ---
    SP_PROMO_TITLE = (By.XPATH, "(//h3[@class='brandDetails__mainSectionTitle'])[1]")

    # --- Share banners ---
    SHARE_BANNERS_TITLE = (By.XPATH, "//h3[@class='brandDetails__mainSectionTitle']")

    # --- Featured brands ---
    FEATURED_BRAND_TITLE = (By.XPATH, "//h3[@class='featuredBrands__title']")
    FEATURED_BRANDS_CARD = (By.XPATH, "//li[@class='featuredBrands__listItem']")
    FEATURED_BRANDS_LINK = (By.XPATH, "//a[@class='featuredBrands__listItemLink']")
    FEATURED_BRANDS_IMG = (By.XPATH, "//img[@class='baseImage  featuredBrands__listItemLinkImage']")

    # --- Properties ---
    @property
    def category_filter(self): return self.element(self.CATEGORY_FILTER)

    @property
    def category_filter_food(self): return self.element(self.CATEGORY_FILTER_FOOD)

    @property
    def category_filter_clear(self): return self.element(self.CATEGORY_FILTER_CLEAR)

    @property
    def letter_filter_all(self): return self.element(self.LETTER_FILTER_ALL)

    @property
    def letter_filter_b(self): return self.element(self.LETTER_FILTER_B)

    @property
    def letter_filter_clear(self): return self.element(self.LETTER_FILTER_CLEAR)

    @property
    def search_by_brand(self): return self.element(self.SEARCH_BY_BRAND)

    @property
    def search_by_brand_input(self): return self.element(self.SEARCH_BY_BRAND_INPUT)

    @property
    def search_by_brand_result(self): return self.element(self.SEARCH_BY_BRAND_RESULT)

    @property
    def search_by_brand_no_result(self): return self.element(self.SEARCH_BY_BRAND_NO_RESULT)

    @property
    def search_by_brand_clear(self): return self.element(self.SEARCH_BY_BRAND_CLEAR)

    @property
    def search_result_letters(self): return self.element(self.SEARCH_RESULT_LETTERS)

    @property
    def search_result_brands(self): return self.element(self.SEARCH_RESULT_BRANDS)

    @property
    def search_result_first(self): return self.element(self.SEARCH_RESULT_FIRST)

    @property
    def search_result_letter_a(self): return self.element(self.SEARCH_RESULT_LETTER_A)

    @property
    def search_result_letter_b(self): return self.element(self.SEARCH_RESULT_LETTER_B)

    @property
    def search_result_bean_box(self): return self.element(self.SEARCH_RESULT_BEAN_BOX)

    @property
    def brand_url(self): return self.element(self.BRAND_URL)

    @property
    def cat_filter(self): return self.element(self.CAT_FILTER)

    @property
    def search_by_brand_input_results(self): return self.element(self.SEARCH_BY_BRAND_INPUT_RESULTS)

    @property
    def build_link_form_title(self): return self.element(self.BUILD_LINK_FORM_TITLE)

    @property
    def landing_page_link_form_title(self): return self.element(self.LANDING_PAGE_LINK_FORM_TITLE)

    @property
    def generate_homepage_link_btn(self): return self.element(self.GENERATE_HOMEPAGE_LINK_BTN)

    @property
    def url_input(self): return self.element(self.URL_INPUT)

    @property
    def short_url_btn(self): return self.element(self.SHORT_URL_BTN)

    @property
    def create_btn(self): return self.element(self.CREATE_BTN)

    @property
    def create_another_btn(self): return self.element(self.CREATE_ANOTHER_BTN)

    @property
    def aff_tracking_input(self): return self.element(self.AFF_TRACKING_INPUT)

    @property
    def short_url_checkbox(self): return self.element(self.SHORT_URL_CHECKBOX)

    @property
    def create_link_btn(self): return self.element(self.CREATE_LINK_BTN)

    @property
    def no_option(self): return self.element(self.NO_OPTION)

    @property
    def created_link(self): return self.element(self.CREATED_LINK)

    @property
    def copy_btn(self): return self.element(self.COPY_BTN)

    @property
    def fb_share(self): return self.element(self.FB_SHARE)

    @property
    def x_share(self): return self.element(self.X_SHARE)

    @property
    def link_copied_msg(self): return self.element(self.LINK_COPIED_MSG)

    @property
    def error_msg(self): return self.element(self.ERROR_MSG)

    @property
    def error_msg_text(self): return self.element(self.ERROR_MSG_TEXT)

    @property
    def not_supported_msg(self): return self.element(self.NOT_SUPPORTED_MSG)

    @property
    def homepage_link_short_link(self): return self.element(self.HOMEPAGE_LINK_SHORT_LINK)

    @property
    def homepage_link_long_link(self): return self.element(self.HOMEPAGE_LINK_LONG_LINK)

    @property
    def short_copy_btn(self): return self.element(self.SHORT_COPY_BTN)

    @property
    def long_copy_btn(self): return self.element(self.LONG_COPY_BTN)

    @property
    def brand_logo(self): return self.element(self.BRAND_LOGO)

    @property
    def brand_title(self): return self.element(self.BRAND_TITLE)

    @property
    def brand_url_link(self): return self.element(self.BRAND_URL)  # avoiding duplicate name

    @property
    def brand_earnings(self): return self.element(self.BRAND_EARNINGS)

    @property
    def brand_cookie_len(self): return self.element(self.BRAND_COOKIE_LEN)

    @property
    def sp_promo_title(self): return self.element(self.SP_PROMO_TITLE)

    @property
    def share_banners_title(self): return self.element(self.SHARE_BANNERS_TITLE)

    @property
    def featured_brand_title(self): return self.element(self.FEATURED_BRAND_TITLE)

    @property
    def featured_brands_card(self): return self.element(self.FEATURED_BRANDS_CARD)

    @property
    def featured_brands_link(self): return self.element(self.FEATURED_BRANDS_LINK)

    @property
    def featured_brands_img(self): return self.element(self.FEATURED_BRANDS_IMG)

    @property
    def loading_dots(self): return self.element(self.LOADING_DOTS)


    def search_brands(self, brand_url):
        # needs https://www.address.com it will extract brand name from url.
        brand_name = get_br_name(brand_url)[:4] if 'www.' in brand_url else brand_url

        #Open the brand filter dropdown, type, then pick the first results
        self.search_by_brand.click()
        sleep(5.5)  # small debounce for results to populate (keep if needed)
        #self.search_by_brand_input.is_displayed()
        self.search_by_brand_input.clear_all()
        self.search_by_brand_input.type(brand_name)
        sleep(0.5)  # small debounce for results to populate (keep if needed)
        self.search_by_brand_result.click()

    def brand_doesnt_exist(self, context, brand_url):
        # requires https://www.address.com (extract full brand name)
        brand_name = get_br_name(brand_url)

        # navigate to Brands
        context.home_page.side_menu_navigate('brands')
        check_spinner(context.driver)

        # open search, type brand, and assert "no results"
        self.search_by_brand.click()
        self.search_by_brand_input.clear_all()
        self.search_by_brand_input.type(brand_name)
        sleep(0.5)  # small debounce for results to render

        return self.search_by_brand_no_result.is_visible()