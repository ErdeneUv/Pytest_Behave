from selenium.webdriver.common.by import By


class PromoPage:
    def __init__(self, driver):
        self.driver = driver

        self.page_title = (By.XPATH, '//h1')

        #search elements:
        self.search_input = (By.XPATH, '//input[@name="search-input"]')
        self.brands_dropdown = (By.XPATH, "(//div[@class = 'c-byKVTi trigger'])[1]")
        self.brands_filter_input = (By.XPATH, "//div[@class='css-1espenb']/input")
        self.brands_filter_result = (By.XPATH, "//div[@role='option']")
        self.sort_dropdown =  (By.XPATH, "(//div[@class = 'c-byKVTi trigger'])[2]")
        self.sort_end_date = (By.XPATH, "//div[.='End Date']")
        self.order_dropdown = (By.XPATH, "(//div[@class = 'c-byKVTi trigger'])[3]")
        self.order_oldest = (By.XPATH, "//div[.= 'Oldest']")
        self.filter_btn = (By.XPATH, '//button[.="Filter"]')
        self.export_btn = (By.CLASS_NAME, "c-cFQNyC-hyvuql-type-export")
        self.brand_url = By.XPATH, "//a[@class='c-gemCGl']"

        #tile elements:
        self.first_tile_generate_btn = (By.XPATH, "(//button[.='Create Link'])[1]")
        self.first_brand_title = (By.XPATH, "(//a[@class='promotionCard__titleLink'])[1]")
        self.created_link = (By.XPATH, "(//span[@class='buttonCopy__affLink'])[1]")
        self.copy_link_btn = (By.XPATH, "(//span[@class='baseIcon buttonCopy__icon'])[1]")
        self.link_generated_btn = (By.XPATH, "//button[@class='baseButton baseButton--primary baseButton--small  buttonCreate buttonsCreateCopy__create']")
        self.fb_share_btn = (By.XPATH, "(//button[contains(@class, 'shareActions__shareFacebook')])[1]")
        self.x_share_btn = (By.XPATH, "(//button[contains(@class, 'shareActions__shareTwitter')])[1]")

        # popup
        self.popup_iframe = (
            By.XPATH, "//div[@class='beamerAnnouncementPopupContainer beamerAnnouncementPopupActive']/iframe")
        self.popup_close_btn = (By.XPATH, '//*[@role="listitem"]/div[4]')

