from time import sleep

from selenium.common import ElementNotInteractableException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def click_on_element(context, element):
    btn = context.driver.find_element(*element)
    wait = WebDriverWait(context.driver, 5)
    wait.until(ec.element_to_be_clickable(btn))
    context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
    #print(f"CLICKED ON THE ELEMENT\n\n\n")
    context.driver.execute_script("arguments[0].click();", btn)

    #actions = ActionChains(context.driver)
    #actions.click(btn).perform()
    #print(F"ACTION PERFORMED...\n\n\n")

