import json
import os
from datetime import datetime
import time
from pathlib import Path
from typing import Optional
from selenium.common import TimeoutException, NoSuchElementException, NoSuchFrameException, \
    StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tests.pages.home_page import HomePage
from tests.utilities.click_on_element import click_on_element
from selenium.webdriver.support import expected_conditions as ec




def check_spinner(driver):
    home_page = HomePage(driver)
    wait = WebDriverWait(driver, 10, poll_frequency=0.5)
    wait.until(ec.invisibility_of_element_located(home_page.spinner))

def check_loading_dots(driver, settle_ms=200):
    home_page = HomePage(driver)
    wait = WebDriverWait(driver, 10, poll_frequency=0.5, ignored_exceptions=[StaleElementReferenceException])

    try:
        appeared = False
        try:
            WebDriverWait(driver, 2, poll_frequency=0.5).until(ec.presence_of_element_located(home_page.loading_dots))
            appeared = True
        except Exception:
            pass
        if appeared:
            wait.until(ec.invisibility_of_element_located(home_page.loading_dots))
    except TimeoutException:
        # If it timed out but the element isn't even present, treat as OK; otherwise, bubble up.
        try:
            if WebDriverWait(driver, 0.5).until(
                    ec.presence_of_element_located(home_page.loading_dots)
            ):
                raise
        except Exception:
            pass  # not present -> OK

        # Tiny settle so the UI can finish painting (prevents flakiness)
    if settle_ms:
        time.sleep(settle_ms / 1000.0)

def close_beamer(context):
    try:
        # print("Closing Beamer\n\n")
        wait = WebDriverWait(context.driver, 3, poll_frequency=0.5)
        wait.until(ec.presence_of_element_located(context.home_page.beamer_iframe))
        # print("trying to get beamer iframe..\n\n")
        context.driver.switch_to.frame(context.driver.find_element(*context.home_page.beamer_iframe))
        # print("tried to get beamer iframe..\n\n")
        click_on_element(context, context.home_page.beamer_close)
        context.driver.switch_to.default_content()
        # print("Beamer is closed\n\n")
    except (TimeoutException, NoSuchElementException, NoSuchFrameException) as e:
        print(f"Beamer notification didn't pop up, continuing on homepage\n")


def date_conversion(date):
    date_str = date

    # Parse string into a datetime object
    dt = datetime.strptime(date_str, "%m/%d/%Y")
    return {
        "year": str(dt.year),  # year as string
        "month": dt.strftime("%B"),  # full month name
        "day": dt.day  # day as int
    }
"""
    parts = date_conversion(date_str)
    
    year = parts["year"]   # "2025"
    month = parts["month"] # "September"
    day = parts["day"]     # 1

"""

def select_date(context, date):
    # month needs to be like "November"
    parts = date_conversion(date)
    year = parts["year"]
    month = parts["month"]
    day = parts["day"]

    is_picked = False
    while not is_picked:
        context.home_page.date_picker_month_prev = (
            By.XPATH, "//button[@class='react-datepicker__navigation react-datepicker__navigation--previous']")
        context.actions = ActionChains(context.driver)

        if month in context.driver.find_element(*context.home_page.date_picker_current_month).text:
            is_picked = True
        else:
            context.actions.click(context.driver.find_element(*context.home_page.date_picker_month_prev)).perform()

    context.wait.until(ec.element_to_be_clickable(context.home_page.date_picker_yr))
    click_on_element(context, context.home_page.date_picker_yr)
    if year in context.driver.find_element(*context.home_page.date_picker_selected_yr).text:
        click_on_element(context, context.home_page.date_picker_selected_yr)
    else:
        target_yr = (By.XPATH, f"//div[.='{year}']")
        click_on_element(context, target_yr)

    day_element = f"//div[.={str(day)}]"
    day_to_click = context.driver.find_elements(By.XPATH, day_element)

    if day <= 10:
        idx = 0
    elif day >= 21:
        idx = 1 if len(day_to_click) > 1 else 0
    else:
        idx = 0

    context.actions.click(day_to_click[idx]).perform()


def err_msg_assert(context, err_txt):
    assert context.brands_page.error_msg.is_displayed()
    actual_err_txt = context.brands_page.error_msg_text.get_text()
    assert err_txt in actual_err_txt, f'actual msg was {actual_err_txt}, expected {err_txt}'

def month_counter(start_date, end_date):
    d1 = datetime.strptime(start_date, "%B %d, %Y")
    d2 = datetime.strptime(end_date, "%B %d, %Y")

    if d1 > d2:
        d1, d2 = d2, d1

    months = (d2.year - d1.year) * 12 + (d2.month - d1.month)

    if d2.day < d1.day:
        months -= 1

    return months


def latest_file_in(folder: Path) -> Optional[Path]:
    files = [p for p in folder.glob("*") if p.is_file()]
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


TEMP_PREFIXES = (".", ".org.chromium.")  # hidden dotfiles, MS Office temp
TEMP_SUFFIXES = (".crdownload", ".part", ".partial", ".tmp", ".")

def is_temp_name(name: Path) -> bool:
    n = name.name.lower()
    return n.startswith(TEMP_PREFIXES) or any(n.endswith(suf) for suf in TEMP_SUFFIXES)


def wait_for_new_file(download_dir: Path, before_timestamp: float, timeout: int = 360) -> Path:
    """
    Wait for a NEW, non-temp file (mtime > before_timestamp) whose size is stable
    for `settle_seconds`. Works locally and on Grid (shared volume).
    """
    end = time.time() + timeout
    settle_seconds = 1.0
    while time.time() < end:
        # pick newest file strictly after the marker and not a temp/hidden name
        cand = None
        newest_ts = -1.0

        for p in download_dir.iterdir():
            if not p.is_file() or is_temp_name(p):
                continue
            try:
                st = p.stat()
            except FileNotFoundError:
                continue
            if st.st_mtime > before_timestamp and st.st_mtime > newest_ts:
                newest_ts, cand = st.st_mtime, p

        if cand:
            print(f'last file name: {cand.name}\n\n')
            try:
                size1 = cand.stat().st_size
                print(f'size1: {size1}')
            except FileNotFoundError:
                time.sleep(0.25); continue

            if size1 > 0:
                time.sleep(settle_seconds)
                try:
                    size2 = cand.stat().st_size
                    print(f'size2: {size2}')
                except FileNotFoundError:
                    time.sleep(0.25); continue

                if size2 == size1:
                    return cand  # finished file

        time.sleep(0.25)

        # One last dump to help debug CI
    try:
        names = ", ".join(sorted([e.name for e in download_dir.iterdir()]))
    except Exception:
        names = "<unreadable>"
    raise AssertionError(
        f"No stable new file appeared under {download_dir} within {timeout}s; final dir listing: [{names}]")


def wait_cdp_download_completed(driver, timeout=180):
    """
    Wait for Chrome DevTools to report the download completed.
    Requires Chrome options: goog:loggingPrefs: {performance: 'ALL'}.
    Works over Remote (Selenium Grid).
    """
    end = time.time() + timeout
    while time.time() < end:
        for entry in driver.get_log("performance"):
            try:
                msg = json.loads(entry["message"])["message"]
                if msg.get("method") == "Browser.downloadProgress":
                    params = msg.get("params", {})
                    if params.get("state") == "completed":
                        return True
            except Exception:
                pass
        time.sleep(0.25)
    raise AssertionError("DevTools did not report download completed within timeout")

def current_time_marker(download_dir: Path) -> float:
    """
    Get a time marker slightly ahead of current last-modified file.
    We use this to detect a *new* file after clicking Export.
    """
    last = latest_file_in(download_dir)
    return (last.stat().st_mtime if last else time.time()) + 0.001

def _resolve_download_dir_from_driver(context) -> Path:
    """
    Prefer the driver-stashed path; fallback to env; then default project path.
    """
    driver_dir = getattr(context.driver, "_download_dir", None)
    if driver_dir:
        return Path(driver_dir)
    env_dir = os.getenv("DOWNLOAD_DIR")
    if env_dir:
        return Path(env_dir)
    return Path("tests/utilities/test_data").resolve()

def wait_dom_ready(driver, timeout=20):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
