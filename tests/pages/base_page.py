from selenium.webdriver.support.ui import WebDriverWait
from .elements import Element
from selenium.webdriver.support import expected_conditions as ec

class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout

    def element(self, locator, timeout=None):
        return Element(self.driver, locator, timeout or self.timeout)

    def elements(self, locator, timeout=None):
        # Return plain WebElements list, but still with a wait
        # Accept either a locator tuple or an Element wrapper
        if isinstance(locator, Element):
            locator = locator.locator
        wait = WebDriverWait(self.driver, timeout or self.timeout, poll_frequency=0.2)
        return wait.until(ec.presence_of_all_elements_located(locator))

    # Some common waits you’ll reuse everywhere
    def wait_url_contains(self, fragment, timeout=None):
        (timeout and WebDriverWait(self.driver, timeout) or self.wait) \
            .until(lambda d: fragment in d.current_url)
