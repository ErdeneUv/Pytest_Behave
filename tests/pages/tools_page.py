from selenium.webdriver.common.by import By


class ToolsPage:
    def __init__(self, driver):
        self.driver = driver
        self.build_tab = (By.XPATH, "(//a[@href='/build-a-link'])[1]")

        #Build A Link tab
        self.url_input = (By.XPATH, "//input[@type='url']")
        self.aff_tracking = (By.XPATH, "//input[@type='text']")
        self.short_url_checkbox = (By.XPATH, "//button[@id='deepLinking']")
        self.create_dlink_btn = (By.XPATH, "//button[.='CREATE DEEP LINK']")
        self.deeplink_output = (By.CLASS_NAME, 'deepLinkForm__yourLink')
        self.build_another_btn = (By.XPATH, "//button[.='Build Another Link']")
        self.created_msg = (By.XPATH, "//p[@class='deepLinkForm__disclaimer']")
        self.empty_error_msg = (By.CLASS_NAME, 'c-jyKkBQ')
        self.err_msg = (By.XPATH, "//p[@class='deepLinkForm__error']")
        self.copy_link_btn = (By.XPATH, "//a[@class='copyLink__link']")
        self.link_copied = (By.XPATH, "//div[.='Link Copied']")
        self.other_brands_link = (By.XPATH, "//div[contains(text(), 'See all other brands')]")
        self.popup_iframe = (
        By.XPATH, "//div[@class='beamerAnnouncementPopupContainer beamerAnnouncementPopupActive']/iframe")
        self.popup_close_btn = (By.XPATH, "//*[@role='listitem']/div[4]")
        self.spinner = (By.XPATH, "//span[@class='loadingOverlay__icon']")


