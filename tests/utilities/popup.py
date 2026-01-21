from tests.utilities.click_on_element import click_on_element
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

def popup(context, iframe, close_btn):
    try:
        WebDriverWait(context.driver, 3).until(ec.frame_to_be_available_and_switch_to_it(iframe))
        WebDriverWait(context.driver, 1.5).until(ec.element_to_be_clickable(close_btn))
        click_on_element(context, close_btn)
        context.driver.switch_to.default_content()
    except TimeoutException:
        print("--------------------------------iFrame did not appear. Executing the next step")