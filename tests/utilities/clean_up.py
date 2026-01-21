import logging
import os
import platform
from datetime import datetime, timedelta
from pathlib import Path, PurePath
from dotenv import find_dotenv
import stat

logger = logging.getLogger()

def get_root_path():
    """
    Uses ENVIRONMENT's value to determine where it lives and returns path to root of the repo
    """
    system = platform.system().lower()
    # macOS:
    if system == "darwin":
        # find_dotenv() returns the full path to your .env file
        from dotenv import find_dotenv
        dotenv_path = find_dotenv(usecwd=True)
        return Path(dotenv_path).parent

    # pipeline
    if os.path.exists("/test-automation"):
        return Path("/test-automation")

def clear_file(file_path, max_days_old = 2):
    """
    Clearing out old failed test cases from rerun.features file
    :param file_path: path to the file
    :param max_days_old: cut off for clear out
    :return: None it would just clear out given files content
    """
    if not os.path.exists(file_path):
        return False

    current_time = datetime.now()
    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    file_age = current_time - mod_time
    # Convert timedelta to days
    days_old = file_age.days

    if days_old >= max_days_old:
        with open(file_path, 'w') as file:
            pass
            logger.info(f'File cleaned up: {file_path}')


def clear_folder(directory,  days_old):
    """
    Simply delete all files from given directories. Deleting all files to avoid multiple files with same names since they're created automatically
    :param directory: list of directory paths to clean.
    :param days_old: days old to clean.
    """

    current_time = datetime.now()
    week_old = current_time - timedelta(days=days_old)

    if not os.path.exists(directory):
        logger.info(f'Directory is not found: {directory}\n')
        return

    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

            if file_mod_time < week_old:
                try:
                    os.chmod(file_path, stat.S_IWRITE)
                    os.remove(file_path)
                except Exception as e:
                    print(f'Error on: {file_path}: {e}')
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(str(dir_path)):
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    print(f'Error on: {dir_path}: {str(e)}')



def cleanup_after_scenario(context):
    """
    Called in after_scenario() to clean up old files.
    it will check ENVIRONMENT variable to see where to start looking up the folders and files
    """
    p_root = get_root_path()

    screenshot_dir = Path.joinpath(PurePath(p_root), 'tests/screenshots')
    report_dir = Path.joinpath(PurePath(p_root), 'tests/test-reports')
    allure_results_dir = Path.joinpath(PurePath(p_root), 'allure-results')
    rerun_feature_dir = Path.joinpath(PurePath(p_root), 'rerun.features')

    clear_folder(screenshot_dir, 7)
    clear_folder(report_dir, 7)
    clear_folder(allure_results_dir, 7)
    clear_file(rerun_feature_dir)

    logger.info("File cleanup completed.\n")

