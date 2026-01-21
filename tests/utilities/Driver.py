import logging
import os
from pathlib import Path
from threading import local
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import  DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.safari.options import Options as SafariOptions

from tests.utilities.final_url import get_ua

# Thread-local storage for driver instances(DriverPool)
driver_pool = local()

def _download_dir_for(browser_type: str) -> str:
    """
    Choose a writable download directory.
    - Local (chrome/chrome_headless): DOWNLOAD_DIR or tests/utilities/test_data
    - Remote (remote_chrome): DOWNLOAD_DIR or /shared-downloads (Docker volume)
    """
    if browser_type == "remote_chrome":
        return os.getenv("DOWNLOAD_DIR", "/shared-downloads")
    return os.getenv("DOWNLOAD_DIR") or str(Path("tests/utilities/test_data").resolve())

def _enable_chrome_downloads_via_cdp(driver: RemoteWebDriver, download_dir: str) -> None:
    """
    Ask Chrome (via CDP) to allow direct downloads to download_dir.
    Some remote/grid builds may no-op; that's fine — prefs still cover most cases.
    """
    try:
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": download_dir
        })
        driver.execute_cdp_cmd("Page.enable", {})
    except Exception:
        # CDP not available on some remotes; ignore silently
        pass

class Driver:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Driver, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    @classmethod
    def get_driver(cls):
        logger = logging.getLogger()

        # Checking if the driver for this thread is already created
        if not hasattr(driver_pool, 'driver') or driver_pool.driver is None:
            browser_type = os.getenv('BROWSER', 'chrome_headless').lower()

            if browser_type == 'chrome':
                user_agents = "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                #print(f'RANDOM DESKTOP USER AGENT: {user_agent}\n\n')
                logger.info(f'RANDOM DESKTOP USER AGENT: {user_agents}\n\n')
                download_dir = _download_dir_for(browser_type)
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument(f'user-agent={user_agents}')
                chrome_options.add_argument('--start-maximized')

                # Add any Chrome-specific options here
                prefs = {
                    "profile.managed_default_content_settings.clipboard": 1,
                    # Download behavior:
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                    "plugins.always_open_pdf_externally": True
                }
                chrome_options.add_experimental_option('prefs', prefs)
                # options.add_argument("whereIsExtension.crx")

                driver_pool.driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=chrome_options
                )

                # Try to force downloads via CDP as well
                _enable_chrome_downloads_via_cdp(driver_pool.driver, download_dir)
                # Handy for tests to read where files landed
                driver_pool.driver._download_dir = download_dir
                logger.info(f"Chrome download dir: {download_dir}")

            elif browser_type == 'chrome_headless':
                user_agents = "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                #print(f'RANDOM USER AGENT: {user_agents}\n\n')
                logger.info(f'RANDOM DESKTOP USER AGENT: {user_agents}\n\n')
                download_dir = _download_dir_for(browser_type)
                chrome_options = webdriver.ChromeOptions()
                prefs = {
                    "profile.managed_default_content_settings.clipboard": 1,
                    # Download behavior:
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                    "plugins.always_open_pdf_externally": True
                }
                chrome_options.add_argument('--headless=new')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--start-maximized')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--incognito')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_argument(f'user-agent={user_agents}')
                chrome_options.add_experimental_option('prefs', prefs)
                # options.add_argument("whereIsExtension.crx")
                chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
                driver_pool.driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=chrome_options
                )
                _enable_chrome_downloads_via_cdp(driver_pool.driver, download_dir)
                driver_pool.driver._download_dir = download_dir
                logger.info(f"Chrome (headless) download dir: {download_dir}")
            elif browser_type == 'remote_chrome':
                # Remote WebDriver for Selenium-hub
                #print('started creating REMOTE_CHROME webdriver...\n')
                #user_agents = get_ua('chrome')
                user_agents = "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                chrome_options = webdriver.ChromeOptions()
                download_dir = _download_dir_for(browser_type)

                prefs = {
                    "profile.managed_default_content_settings.clipboard": 1,
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                    "plugins.always_open_pdf_externally": True
                }
                chrome_options.add_argument('--headless=new')
                chrome_options.add_argument(f'user-agent={user_agents}')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--incognito')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument("--disable-features=BlockThirdPartyCookies")
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_experimental_option('prefs', prefs)

                driver_pool.driver = webdriver.Remote(
                    command_executor='http://selenium-hub:4444/wd/hub',
                    options=chrome_options
                )
                _enable_chrome_downloads_via_cdp(driver_pool.driver, download_dir)
                driver_pool.driver._download_dir = download_dir
                logger.info(f"Remote Chrome download dir: {download_dir}")

            elif browser_type == 'chrome_sandbox':
                # Remote WebDriver for Selenium-hub
                #print('started creating REMOTE_CHROME webdriver...\n')
                #user_agents = get_ua('chrome')
                user_agents = "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                chrome_options = webdriver.ChromeOptions()
                download_dir = _download_dir_for(browser_type)

                prefs = {
                    "profile.managed_default_content_settings.clipboard": 1,
                    "download.default_directory": download_dir,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                    "plugins.always_open_pdf_externally": True
                }
                chrome_options.add_argument('--headless=new')
                chrome_options.add_argument(f'user-agent={user_agents}')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--incognito')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument("--disable-features=BlockThirdPartyCookies")
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_experimental_option('prefs', prefs)

                driver_pool.driver = webdriver.Remote(
                    command_executor='http://localhost:4444/wd/hub',
                    options=chrome_options
                )
                _enable_chrome_downloads_via_cdp(driver_pool.driver, download_dir)
                driver_pool.driver._download_dir = download_dir
                logger.info(f"Remote Chrome download dir: {download_dir}")

            elif browser_type == 'firefox':
                user_agent = get_ua(browser_type)
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", user_agent)

                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument('--start-maximized')
                firefox_options.set_preference("dom.events.testing.asyncClipboard", True)
                firefox_options.profile = profile

                driver_pool.driver = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=firefox_options
                )

            elif browser_type == 'firefox_headless':
                user_agent = get_ua(browser_type)
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", user_agent)

                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument('--start-maximized')
                firefox_options.add_argument('--headless')
                firefox_options.set_preference("dom.events.testing.asyncClipboard", True)
                firefox_options.profile = profile

                driver_pool.driver = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=firefox_options
                )
            elif browser_type == 'remote_firefox':
                #print('started creating REMOTE_FIREFOX webdriver...\n')
                user_agent = get_ua(browser_type)
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", user_agent)

                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument('--start-maximized')
                firefox_options.add_argument('--headless')
                firefox_options.set_preference("dom.events.testing.asyncClipboard", True)
                firefox_options.profile = profile

                remote_url = 'http://selenium-hub:4444/wd/hub' #remote URL here
                driver_pool.driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=firefox_options
                )
                #print('Remote webdriver is up and running')

            elif browser_type == 'safari':
                user_agent = get_ua(browser_type)
                safari_options = webdriver.SafariOptions()
                safari_options.add_argument(f"--user-agent={user_agent}")
                #safari_options.set_capability('safari:automaticProfiling', True)
                driver_pool.driver = webdriver.Safari(options=safari_options)
                driver_pool.driver.maximize_window()

            elif browser_type == 'safari_headless':
                user_agent = get_ua(browser_type)
                safari_options = webdriver.SafariOptions()
                safari_options.add_argument('--start-maximized')
                safari_options.add_argument(f"--user-agent={user_agent}")
                safari_options.add_argument('--headless')
                #safari_options.set_capability('safari:automaticProfiling', True)
                driver_pool.driver = webdriver.Safari(options=safari_options)

            elif browser_type == 'remote_safari':
                #print('started creating REMOTE_SAFARI webdriver...\n')
                capabilities = DesiredCapabilities.SAFARI.copy()
                capabilities['browserName'] = 'safari_headless'
                remote_url = 'http://selenium-hub:4444/wd/hub' #remote URL here
                driver_pool.driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=capabilities
                )
                #print('Remote webdriver is up and running')

            else:
                raise RuntimeError(
                    f"Unknown browser type {browser_type}."
                )

        return driver_pool.driver

    @classmethod
    def close_driver(cls):
        if hasattr(driver_pool, 'driver') and driver_pool.driver:
            try:
                try:
                    driver_pool.driver.execute_script(
                        "window.localStorage.clear(); window.sessionStorage.clear();"
                    )
                except Exception:
                    pass
                try:
                    driver_pool.driver.delete_all_cookies()
                except Exception:
                    pass
                try:
                    driver_pool.driver.quit()
                except Exception:
                    pass
            finally:
                driver_pool.driver = None
