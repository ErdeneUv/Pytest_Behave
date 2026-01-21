import os
from time import sleep

from selenium.common import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from tests.utilities.Driver import driver_pool
from tests.utilities.click_on_element import click_on_element


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

        #welcome back
        self.username_input = (By.XPATH, "//input[@name='user-input']")
        self.password_input = (By.XPATH, "//input[@name='password-input']")
        self.reset_password = (By.XPATH, "//div[contains(text(), 'Reset password')]")
        self.submit_button = (By.XPATH, "//button[contains(text(), 'SIGN IN')]")
            #(By.CLASS_NAME, "c-hjfmDJ-glfjBG-type-login")
            #(By.XPATH, "//div[contains(@style, 'padding')]/button"),
        #headers and footers
        #self.apply_now_top = self.driver.find_element(By.XPATH, "//a[.='apply now']")
        #self.apply_now_bottom = self.driver.find_element(By.XPATH, "//a[.='Apply for one now']")

        #iframe
        self.iframe_recaptcha = (By.XPATH, "//iframe[@title='reCAPTCHA']")
        self.recaptcha_btn = (By.XPATH, "//div[@class='recaptcha-checkbox-border']")

        #reset
        self.reset_pwd_post_msg = (By.XPATH, "//div[@class='c-hqJias']")
        self.send_btn = (By.XPATH, "//button[.='SEND']")
        self.reset_pwd_msg = (By.XPATH, "//p[contains(text(), 'send you')]")
        self.login_error_msg = (By.CLASS_NAME, "c-jyKkBQ")
        self.back_to_login = (By.CLASS_NAME, "c-goEgdK-fFWopP-type-fourth")
        self.welcome_msg = (By.CLASS_NAME, "c-RaAti")
        self.wait = WebDriverWait(self.driver, 25)

    def recaptcha(self):
        sleep(1)
        self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.iframe_recaptcha))
        self.wait.until(ec.element_to_be_clickable(self.recaptcha_btn))
        self.driver.find_element(*self.recaptcha_btn).click()
        self.driver.switch_to.default_content()
        sleep(2) #sleeps for recaptcha being cleared


    def login(self, username, password):
        #self.wait.until(ec.element_to_be_clickable(self.username_input))
        #self.recaptcha()
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        click_on_element(self, self.submit_button)
        #sleep(0.5)
        #try:
        #    if self.driver.find_element(*self.username_input).is_displayed():
        #        click_on_element(self, self.submit_button)
                #print(f"second click performed\n\n")

        #except (StaleElementReferenceException, Exception):
        #    self.submit_button = (By.XPATH, "//button[contains(text(), 'SIGN IN')]")


    def login_click(self, username, password):
        self.wait.until(ec.element_to_be_clickable(self.username_input))
        #self.recaptcha()
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element(*self.submit_button)).perform()
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.wait.until(ec.presence_of_element_located(self.submit_button))
        while self.driver.find_element(*self.submit_button):
            try:
                click_on_element(self, self.submit_button)
            except (TimeoutException, StaleElementReferenceException, NoSuchElementException) as e:
                pass
            try:
                self.wait.until(ec.visibility_of_element_located(self.submit_button))
                break
            except TimeoutException:
                continue


    def login_by_role_click(self, role: str):
        username = os.environ["USERNAME_" + role.upper()]
        password = os.environ["PWD_" + role.upper()]
        self.login_click(username, password)


    def login_by_role(self, role: str):
        env = os.getenv("ENVIRONMENT")

        username = os.environ["USERNAME_" + role.upper()]
        password = os.environ['PWD_' + role.upper()]

        self.login(username, password)


    def reset_password(self, username):
        click_on_element(self, self.reset_password)
        self.wait.until(ec.element_to_be_clickable(self.username_input))
        self.driver.find_element(*self.username_input).send_keys(username)
        self.wait.until(ec.element_to_be_clickable(self.submit_button))
        click_on_element(self, self.submit_button)


