# setup and teardown test environment, both at the global level, and at each feature and scenario
import os
import logging
from pathlib import Path
import re

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from tests.utilities.clean_up import cleanup_after_scenario, get_root_path
from tests.utilities.Driver import Driver
from tests.utilities.env_loader import load_env_files, project_root


def before_all(context):
    load_env_files()
    root = project_root()
    log_path = Path.joinpath(Path(root), "tests/logs")

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    logger = logging.getLogger()
    logging.basicConfig(
        filename= Path.joinpath(log_path, "test_execution.log"),
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    #logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) #can change to DEBUG
    logger.addHandler(console_handler)

    context.config.setup_logging()
    context.logger = logger
    load_testdata_into_env()



def before_scenario(context, scenario):
    if any('api' in tag for tag in scenario.tags):
        base_url = os.getenv('BASE_URL_API')
        context.driver = None
        context.logger.info(f"\nStarting scenario: {scenario.name}\nAPI Test no webdriver created")
        context.logger.info(f"\nRequest will be sent to {base_url}\n\n")
    else:
        context.logger.info(f"\nStarting scenario: {scenario.name}")
        context.driver = Driver.get_driver()
        #context.logger.info('environment.py getting started with Driver.py')
        url = os.getenv('BASE_URL')
        env = os.getenv('ENVIRONMENT')
        #print(f"Base Url is set to: {url}\nENVIRONMENT: {env}\nBROWSER: {os.getenv('BROWSER')}\nTAGS: {os.getenv('TAGS')}\n\n")
        context.logger.info(f"Base Url is set to: {url}\nENVIRONMENT: {env}\nBROWSER: {os.getenv('BROWSER')}\nTAGS: {os.getenv('TAGS')}\n\n")
        context.driver.set_page_load_timeout(10)
        context.driver.implicitly_wait(2)
        context.wait = WebDriverWait(context.driver, 10)
        context.action = ActionChains(context.driver)
        context.driver.get(url)
    #context.logger.info(f"\nDriver created: {scenario.name}")


def after_scenario(context, scenario):
    context.logger.info(f"Finished scenario: {scenario.name} with status {scenario.status} ")
    # take a screenshot if a scenario fails
    try:
        if scenario.status == 'failed' and any('api' in tag for tag in scenario.tags):
            context.logger.info(f"\nafter_scenario executed: {scenario.name}")

        if scenario.status == 'failed' and not any('api' in tag for tag in scenario.tags):
            try:
                s_shot = context.driver.get_screenshot_as_png()
                try:
                    allure.attach(
                        s_shot,
                        name=f"Failure Screenshot - {scenario.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    print(f'Failed to attach ss to Allure Report: {e}')
                # this is for local runs, container and CI runs are handled by allure.attach
                filename = re.sub(r'[^a-zA-Z0-9_-]', '_', scenario.name) + ".png"
                p_root = get_root_path()
                screenshot_dir = Path(p_root).joinpath("tests", "screenshots")
                filepath = os.path.join(screenshot_dir, filename)
                # Save screenshot
                with open(filepath, "wb") as f:
                    f.write(s_shot)
            except Exception as e:
                print(f'screenshot didnt captured: {e}')
    finally:
        if context.driver is not None:
            Driver.close_driver()



def after_all(context):
    # clean up old screenshots and reports
    cleanup_after_scenario(context)


def _inject_env(k: str, v: str):
    curr = os.environ.get(k)
    if curr is None or curr.strip() == "":
        os.environ[k] = v


def load_testdata_into_env():
    p = Path(os.getenv("TEST_DATA_FILE", "tests/utilities/test_data/testdata.env"))
    if not p.exists():
        return

    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        _inject_env(k.strip(), v.strip())

"""
    # Support .env (key=value), .json (flat object)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise RuntimeError("JSON test data must be a flat object {key: value}.")
        for k, v in data.items():
            if v is None:
                continue
            _inject_env(str(k), str(v))
"""

