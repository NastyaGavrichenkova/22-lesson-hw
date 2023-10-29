import allure
import pytest
from appium import webdriver
from selene import browser, support
import allure_commons
import utils

from config import app_config


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    with allure.step('Init ap session'):
        browser.config.driver = webdriver.Remote(
            app_config.remote_url,
            options=app_config.to_driver_options()
        )

    browser.config.timeout = app_config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    utils.allure.attach_screenshot(browser)

    utils.allure.attach_page_source(browser)

    session_id = browser.driver.session_id

    browser.quit()

    if app_config.runs_on_bstack():
        utils.allure.attach_bstack_video(session_id)