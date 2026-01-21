import re
from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage

class ReportsPage(BasePage):
    # Report buttons
    SUMMARY_REPORT = (By.XPATH, "//button[.='Summary']")
    BRANDS_REPORT = (By.XPATH, "//button[.='Brands']")
    CONVERSION_REPORT = (By.XPATH, "//button[.='Conversion']")
    TRAFFIC_REPORT = (By.XPATH, "//button[.='Traffic']")
    PAYMENT_REPORT = (By.XPATH, "//button[.='Payment']")

    # LPR filters
    BRAND_FILTER_DROPDOWN = (By.XPATH, "//button[@class='multiSelectFilterLimitedDropdown__toggle']")
    BRAND_FILTER_INPUT = (By.XPATH, "//input[@placeholder='Search Brands...']")
    BRAND_FILTER_FIRST_OPTION = (
        By.XPATH, "(//span[@class='multiSelectFilterLimitedDropdown__menuInnerListItemLabelText'])[1]")

    USER_FILTER_DROPDOWN = (By.XPATH, "(//button[@class='multiSelectFilterLimitedDropdown__toggle'])[2]")
    USER_FILTER_INPUT = (By.XPATH, "//input[@class='multiSelectFilterLimitedDropdown__menuSearchInput']")
    USER_FILTER_FIRST_OPTION = (
        By.XPATH, "//label[@class='multiSelectFilterLimitedDropdown__menuInnerListItemLabel']")

    CLEAR_BTN = (By.XPATH, "//button[.='Clear Filters']")

    # LPR table headers
    CREATED_HEADER = (By.XPATH, "//th[1]")
    LINK_HEADER = (By.XPATH, "//th[2]")
    BRAND_HEADER = (By.XPATH, "//th[3]")
    USER_HEADER = (By.XPATH, "//th[4]")
    SALES_HEADER = (By.XPATH, "//th[5]")
    PAYOUT_HEADER = (By.XPATH, "//th[6]")
    CLICKS_HEADER = (By.XPATH, "//th[7]")
    ORDERS_HEADER = (By.XPATH, "//th[8]")

    # LPR 1st row
    SALES_FIRST = (By.XPATH, "(//td[contains(@class, 'reportLink__mainInnerTableCell--sales')])[1]")
    PAYOUT_FIRST = (By.XPATH, "(//td[contains(@class, 'reportLink__mainInnerTableCell--payout')])[1]")
    CLICKS_FIRST = (By.XPATH, "(//td[contains(@class, 'reportLink__mainInnerTableCell--clicks')])[1]")
    ORDERS_FIRST = (By.XPATH, "(//td[contains(@class, 'reportLink__mainInnerTableCell--orders')])[1]")

    # LPR date presets
    TODAY = (By.XPATH, "//button[.='Today']")
    YESTERDAY = (By.XPATH, "//button[.='Yesterday']")
    ONE_W = (By.XPATH, "//button[.='1W']")
    ONE_M = (By.XPATH, "//button[.='1M']")
    THREE_M = (By.XPATH, "//button[.='3M']")
    ONE_Y = (By.XPATH, "//button[.='1Y']")
    MTD = (By.XPATH, "//button[.='MTD']")
    YTD = (By.XPATH, "//button[.='YTD']")
    START_DATE_LPR = (By.XPATH, "//input[@name='startDate']")
    END_DATE_LPR = (By.XPATH, "//input[@name='endDate']")

    # LPR pagination
    LINK_PAG = (By.XPATH, "//div[@class='reportLink__mainPaginationInfo']")
    PAGE_PAG = (By.XPATH, "//span[@class='reportLink__mainPaginationControlsInputPages']")

    # Report filters
    RUN_REPORT_BTN = (By.XPATH, "//button[@data-event='report-page-run-report-btn']")
    RESET_FILTERS_BTN = (By.XPATH, "//button[@data-event='reports-page-reset-filters-btn']")
    EXPORT_AS_CSV = (By.XPATH, "//button[@data-event='report-page-export-as-csv-btn']")

    # --- Properties ---
    @property
    def summary_report(self): return self.element(self.SUMMARY_REPORT)

    @property
    def brands_report(self): return self.element(self.BRANDS_REPORT)

    @property
    def conversion_report(self): return self.element(self.CONVERSION_REPORT)

    @property
    def traffic_report(self): return self.element(self.TRAFFIC_REPORT)

    @property
    def payment_report(self): return self.element(self.PAYMENT_REPORT)

    @property
    def brand_filter_dropdown(self): return self.element(self.BRAND_FILTER_DROPDOWN)

    @property
    def brand_filter_input(self): return self.element(self.BRAND_FILTER_INPUT)

    @property
    def brand_filter_first_option(self): return self.element(self.BRAND_FILTER_FIRST_OPTION)

    @property
    def user_filter_dropdown(self): return self.element(self.USER_FILTER_DROPDOWN)

    @property
    def user_filter_input(self): return self.element(self.USER_FILTER_INPUT)

    @property
    def user_filter_first_option(self): return self.element(self.USER_FILTER_FIRST_OPTION)

    @property
    def clear_btn(self): return self.element(self.CLEAR_BTN)

    @property
    def created_header(self): return self.element(self.CREATED_HEADER)

    @property
    def link_header(self): return self.element(self.LINK_HEADER)

    @property
    def brand_header(self): return self.element(self.BRAND_HEADER)

    @property
    def user_header(self): return self.element(self.USER_HEADER)

    @property
    def sales_header(self): return self.element(self.SALES_HEADER)

    @property
    def payout_header(self): return self.element(self.PAYOUT_HEADER)

    @property
    def clicks_header(self): return self.element(self.CLICKS_HEADER)

    @property
    def orders_header(self): return self.element(self.ORDERS_HEADER)

    @property
    def sales_first(self): return self.element(self.SALES_FIRST)

    @property
    def payout_first(self): return self.element(self.PAYOUT_FIRST)

    @property
    def clicks_first(self): return self.element(self.CLICKS_FIRST)

    @property
    def orders_first(self): return self.element(self.ORDERS_FIRST)

    @property
    def today(self): return self.element(self.TODAY)

    @property
    def yesterday(self): return self.element(self.YESTERDAY)

    @property
    def one_w(self): return self.element(self.ONE_W)

    @property
    def one_m(self): return self.element(self.ONE_M)

    @property
    def three_m(self): return self.element(self.THREE_M)

    @property
    def one_y(self): return self.element(self.ONE_Y)

    @property
    def mtd(self): return self.element(self.MTD)

    @property
    def ytd(self): return self.element(self.YTD)

    @property
    def start_date_lpr(self): return self.element(self.START_DATE_LPR)

    @property
    def end_date_lpr(self): return self.element(self.END_DATE_LPR)

    @property
    def link_pag(self): return self.element(self.LINK_PAG)

    @property
    def page_pag(self): return self.element(self.PAGE_PAG)

    @property
    def run_report_btn(self): return self.element(self.RUN_REPORT_BTN)

    @property
    def reset_filters_btn(self): return self.element(self.RESET_FILTERS_BTN)

    @property
    def export_as_csv(self): return self.element(self.EXPORT_AS_CSV)

    # custom methods for Reports pages
    def lpr_sort(self, header):
        header_map = {
            "created": self.created_header,
            "link": self.link_header,
            "brand": self.brand_header,
            "user": self.user_header,
            "sales": self.sales_header,
            "payout": self.payout_header,
            "clicks": self.clicks_header,
            "orders": self.orders_header,
        }

        key = header.strip().lower()
        if key not in header_map:
            raise ValueError(f"Invalid header '{header}'. Must be one of: {list(header_map.keys())}")

        header_element = header_map[key]
        header_element.click()

    def get_total_links(self, el):
        # Prefer .text (Selenium normalizes a bit), then fall back
        raw = (el.get_text or el.get_attribute("innerText") or el.get_attribute("textContent") or "").strip()

        # Normalize Unicode spaces (NBSP, thin space, zero-width, etc.)
        raw = re.sub(r"[\u00A0\u202F\u2009\u2007\u200A\u200B]", " ", raw)
        raw = re.sub(r"\s+", " ", raw)

        # Try: last number right before the word 'links'
        m = re.search(r"(\d[\d,]*)\s*links?$", raw, flags=re.I)
        if m:
            return int(m.group(1).replace(",", ""))

        # Fallback: take the last number anywhere in the string
        nums = re.findall(r"\d[\d,]*", raw)
        return int(nums[-1].replace(",", "")) if nums else None