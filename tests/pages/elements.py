from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Element:
    """Wraps a locator and driver; waits just-in-time before interacting."""
    def __init__(self, driver, locator, timeout=15):
        self.driver = driver
        self.locator = locator
        self.timeout = timeout

    def _wait(self, condition):
        return WebDriverWait(self.driver, self.timeout, poll_frequency=0.2).until(condition(self.locator))

    def _scroll_into_view(self, el):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass

    @property
    def webelement(self):
        # Use presence; upgrade to visibility/clickable where needed
        return self._wait(EC.presence_of_element_located)

    def get_text(self):
        return self.webelement.text

    def click(self):
        el = self._wait(EC.element_to_be_clickable)
        self._scroll_into_view(el)
        #el = el.webelement
        self.driver.execute_script("arguments[0].click();", el)
        #action = ActionChains(self.driver)
        #action.move_to_element(el).perform()
        #action.click(el).perform()

    def type(self, text):
        el = self._wait(EC.visibility_of_element_located)
        el.send_keys(text)

    def clear_all(self):
        el = self._wait(EC.element_to_be_clickable)  # same pattern as your click/type
        el.click()

        # Try Ctrl/Cmd+A then Delete
        for mod in (Keys.CONTROL, Keys.COMMAND):
            try:
                el.send_keys(mod, 'a')
                el.send_keys(Keys.DELETE)  # or Keys.BACKSPACE
                if (el.get_attribute('value') or '').strip() == '':
                    return
            except Exception:
                pass

        # Fallback: select from end → start, then Backspace
        el.send_keys(Keys.END)
        el.send_keys(Keys.SHIFT, Keys.HOME)
        el.send_keys(Keys.BACKSPACE)

    def is_visible(self):
        try:
            self._wait(EC.visibility_of_element_located)
            return True
        except Exception:
            return False

    def is_invisible(self):
        try:
            self._wait(EC.invisibility_of_element)
            return True
        except Exception:
            return False

    def is_present(self):
        try:
            self._wait(EC.presence_of_element_located)
            return True
        except Exception:
            return False

    def get_attribute(self, attribute):
        el = self._wait(EC.presence_of_element_located)
        return el.get_attribute(attribute)

    def is_displayed(self):
        try:
            el = self._wait(EC.visibility_of_element_located)
            return el.is_displayed()
        except Exception:
            return False

    def get_dom_attribute(self, attribute):
        el = self._wait(EC.presence_of_element_located)
        return el.get_dom_attribute(attribute)