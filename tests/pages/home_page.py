import logging
import os
from os import error
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from tests.utilities.click_on_element import click_on_element


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        self.notifications_btn = (By.XPATH, "//a[@href='https://app.getbeamer.com/brandcycle']")
        self.support_btn = (By.XPATH, "//a[@href='/contact-support']")
        self.account_dashboard_btn = (By.XPATH, "//span[contains(text(), 'Welcome')]")
        self.logout = (By.XPATH, "(//a[@href='/logout'])[2]")

        #side nav bar
        self.home_page = (By.XPATH, "//a[@class='navMain__logo']")
        self.brands_menu = (By.XPATH, "(//span[.='Brands'])[1]")
        self.trending = (By.XPATH, "(//span[.='Trending'])[1]")
        self.collections = (By.XPATH, "(//span[@class='navMainList__itemLinkText'])[4]")
        self.promotions_menu = (By.XPATH, "(//span[.='Promotions'])[1]")
        self.reports_menu = (By.XPATH, "//button[@aria-controls='dropdown-reports']")
        self.reports_summary = (By.XPATH, "//ul[@id='dropdown-reports']//span[contains(text(), 'Summary')]")
        self.link_performance = (By.XPATH, "//span[contains(text(), 'Link Performance')]")
        self.reports_brands = (By.XPATH, "//ul[@id='dropdown-reports']//span[contains(text(), 'Brands')]")
        self.reports_conversion = (By.XPATH, "//ul[@id='dropdown-reports']//span[contains(text(), 'Conversion')]")
        self.reports_traffic_referral = (By.XPATH, "//ul[@id='dropdown-reports']//span[contains(text(), 'Traffic Referrals')]")
        self.reports_payment = (By.XPATH, "//ul[@id='dropdown-reports']//span[contains(text(), 'Payment')]")
        self.payment_balance = (By.XPATH, "//ul[@id='dropdown-reports']//span[contains(text(), 'Payment Balance')]")
        self.referral_link = (By.XPATH, "//ul[@id='dropdown-reports']//span[contains(text(), 'Referral Links')]")
        self.tools_menu = (By.XPATH, "(//span[.='Tools'])[1]")
        self.blog_menu = (By.XPATH, "(//span[.='Blog'])[1]")
        self.support_menu = (By.XPATH, "(//span[.='Support'])[1]")

        #Build A Link
        self.build_form_title = (By.XPATH, "//h3[@class='deepLinkForm__title']")
        self.url_input = (By.XPATH, "//input[@type='url']")
        self.aff_tracking = (By.XPATH, "//input[@type='text']")
        self.short_url_btn = (By.XPATH, "//button[@id='deepLinking']")
        self.create_dlink_btn = (By.XPATH, "//button[@data-event='homepage-create-link-btn']")
        self.deeplink_output = (By.CLASS_NAME, 'deepLinkForm__yourLink')
        self.link_copied = (By.CLASS_NAME, 'copyDisclaimer')
        self.build_another_btn = (By.CLASS_NAME, 'c-kHhrBF')
        self.empty_error_msg = (By.XPATH, "//*[contains(text(), 'Destination URL can not be empty')]")
        self.err_msg = (By.CLASS_NAME, 'deepLinkForm__error')
        self.copy_link_btn = (By.XPATH, '//a[.="Copy Link"]')
        self.other_brands_link = (By.XPATH, "//div[contains(text(), 'See all other brands')]")

        #Pop ups and Spinners of Build a Link
        self.popup_iframe = (By.XPATH, "//div[@class='beamerAnnouncementPopupContainer beamerAnnouncementPopupActive']/iframe")
        self.popup_close_btn = (By.XPATH, '//*[@role="listitem"]/div[4]')
        self.spinner = (By.XPATH, "//div[@data-test='spinner-deeplink']")
        self.loading_dots = (By.XPATH, "//div[@class='loadingDots baseButton__loading']")

        #Snapshot Report
        self.snapshot_title = (By.XPATH, "//h2[@class='snapshotReport__title']")
        self.calendar_snapshot = (By.XPATH, "//input[@type='date']")
        self.date_preset = (By.XPATH, "//div[@class='c-byKVTi trigger']")
        self.between_dates = (By.XPATH, "//div[.='Between Dates']")
        self.today = (By.XPATH, "//div[.='Today']")
        self.yesterday = (By.XPATH, "//div[.='Yesterday']")
        self.last_seven_days = (By.XPATH, "//div[.='Last 7 Days']")
        self.this_month = (By.XPATH, "//div[.='This Month']")
        self.last_month = (By.XPATH, "//div[.='Last Month']")
        self.this_year = (By.XPATH, "//div[.='This Year']")
        self.last_year = (By.XPATH, "//div[.='Last Year']")

        self.start_date_input = (By.XPATH, "//input[@placeholder='Start Date']")
        self.date_picker_yr = (By.CLASS_NAME, 'react-datepicker__year-read-view--selected-year' )
        self.date_picker_selected_yr = (By.XPATH, "//div[@aria-selected='true']")
        self.date_picker_yr_2025 = (By.XPATH, "//div[.='2025']")
        self.date_picker_yr_2024 = (By.XPATH, "//div[.='2024']")
        self.date_picker_month_prev = (By.XPATH, "//button[@class='react-datepicker__navigation react-datepicker__navigation--previous']")
        self.date_picker_month_next = (By.XPATH, "//button[@aria-label='Next Month']")

        self.date_picker_current_month = (By.CLASS_NAME, 'react-datepicker__current-month')
        self.date_picker_day = (By.XPATH, "//div[.='1']")
        self.date_picker_day_end = (By.XPATH, "//div[@aria-label='Choose Wednesday, October 30th, 2024']")

        self.date_picker_middle = (By.XPATH, "//button[@class='react-calendar__navigation__label']")

        self.end_date_input = (By.XPATH, "//input[@placeholder='End Date']")
        #self.end_date_cal_btn = (By.XPATH, '(//span[@class="datePicker__calendarButton"])[2]')
        self.run_btn = (By.XPATH, "//button[.='Run Report']")
        self.clicks_output = (By.XPATH, "(//span[@class='snapshotReportStats__itemValue'])[1]")
        self.orders_output = (By.XPATH, "(//span[@class='snapshotReportStats__itemValue'])[2]")
        self.sales_output = (By.XPATH, "(//span[@class='snapshotReportStats__itemValue'])[3]")
        self.commissions_output = (By.XPATH, "(//span[@class='snapshotReportStats__itemValue'])[4]")

        #Featured Announcements
        self.announcements_head_title = (By.XPATH, "//h2[@class='home__sectionTitle']")
        self.announcements_card = (By.XPATH, "//a[@class='announcementCard__link']")
        self.announcements_title = (By.XPATH, "//h3[@class='announcementCard__linkTitle']")
        self.announcements_img = (By.XPATH, "//img[@alt='Announcement image']")
        self.announcements_body = (By.XPATH, "//p[@class='announcementCard__linkDescription']")
        self.announcements_url = (By.XPATH, "//article[@class='announcementCard home__sectionListItemArticle']")

        #Socials
        self.social_head_title = (By.XPATH, "(//h2[@class='home__sectionTitle'])[2]")
        self.social_instagram_icon = (By.XPATH, "(//li[@class='socialIcons__item'])[1]")
        self.social_fb_icon = (By.XPATH, "(//li[@class='socialIcons__item'])[2]")
        self.social_x_icon = (By.XPATH, "(//li[@class='socialIcons__item'])[3]")

        #Blog
        self.blog_head_title = (By.XPATH, "(//h2[@class='home__sectionTitle'])[3]")
        self.blog_title = (By.XPATH, "//h3[@class='blogCard__linkDetailsTitle']")
        self.blog_date = (By.XPATH, "//p[@class='blogCard__linkDetailsDate']")
        self.blog_img = (By.XPATH, "//img[@alt='Blog image']")
        self.blog_body = (By.XPATH, "//p[@class='blogCard__linkDetailsDescription']")
        self.blog_read_more = (By.XPATH, "//p[@class='blogCard__linkDetailsReadmore']")

        #Bottom elements
        self.footer_social_insta = (By.XPATH, "(//ul[@class='socialIcons']/li)[1]")
        self.footer_social_fb = (By.XPATH, "(//ul[@class='socialIcons']/li)[2]")
        self.footer_social_x = (By.XPATH, "(//ul[@class='socialIcons']/li)[3]")
        self.footer_copy_right = (By.XPATH, "//small[@class='footer__copyright']")

        #beamer notifications
        self.beamer_iframe = (By.ID, "beamerAnnouncementPopup")
        self.beamer_close = (By.XPATH, "//div[@class='popupClose']")

    #functions
    def build_a_link(self, url):
        self.wait.until(ec.element_to_be_clickable(self.url_input))
        self.driver.find_element(*self.url_input).send_keys(url)
        try:
            self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.popup_iframe))
            self.wait.until(ec.element_to_be_clickable(self.popup_close_btn))
            click_on_element(self, self.popup_close_btn)
            self.driver.switch_to.default_content()
        except TimeoutException:
            print("--------------------------------iFrame did not appear. Executing the next step\n\n")


    def error_msg_check(self, msg):
        self.wait.until(
            ec.presence_of_element_located(self.err_msg))
        actual_msg = self.driver.find_element(*self.err_msg).text
        assert msg == actual_msg, f'Message does not match, actual_msg: {actual_msg}'

    def check_spinner(self):
        self.wait.until_not(ec.presence_of_element_located(self.spinner))


    def side_menu_navigate(self, side_menu):
        try:
            #sself.wait.until(ec.element_to_be_clickable(self.brands_menu))
            side_menu = side_menu.lower()
            if "brands" in side_menu:
                click_on_element(self, self.brands_menu)
            elif "promo" in side_menu:
                click_on_element(self, self.promotions_menu)
            elif "trending" in side_menu:
                click_on_element(self, self.trending)
            elif "collections" in side_menu:
                click_on_element(self, self.collections)
            elif "report" in side_menu:
                actions = ActionChains(self.driver)
                actions.move_to_element(self.driver.find_element(*self.reports_menu)).click(self.driver.find_element(*self.reports_menu)).perform()
                self.wait.until(ec.element_to_be_clickable(self.link_performance))
                if "summary" in side_menu:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(self.driver.find_element(*self.reports_summary)).click(self.driver.find_element(*self.reports_summary)).perform()
                elif "link-performance" in side_menu:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(self.driver.find_element(*self.link_performance)).click(self.driver.find_element(*self.link_performance)).perform()
                elif "brand" in side_menu:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(self.driver.find_element(*self.reports_brands)).click(self.driver.find_element(*self.reports_brands)).perform()
                elif "conversion" in side_menu:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(self.driver.find_element(*self.reports_conversion)).click(self.driver.find_element(*self.reports_conversion)).perform()
                elif "traffic" in side_menu:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(self.driver.find_element(*self.reports_traffic_referral)).click(self.driver.find_element(*self.reports_traffic_referral)).perform()
                elif "payment" in side_menu:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(self.driver.find_element(*self.reports_payment)).click(self.driver.find_element(*self.reports_payment)).perform()
                else:
                    raise ValueError(f'This report menu not found {side_menu}')
            elif "tools" in side_menu:
                click_on_element(self, self.tools_menu)
            elif "blog" in side_menu:
                click_on_element(self, self.blog_menu)
            elif "support" in side_menu:
                click_on_element(self, self.support_menu)
            else:
                raise ValueError(f'This report menu not found {side_menu}')

        except TimeoutException as e:
            raise TimeoutError(f'Wait timed out on "side_menu_navigate" in "homepage"\n\n')
