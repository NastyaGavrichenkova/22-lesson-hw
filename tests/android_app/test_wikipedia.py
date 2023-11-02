import allure

from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have

from data import onboarding


def test_run_onboarding():
    page_number = 1

    with allure.step(f'Verify content on the {page_number} screen'):
        text = browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/primaryTextView'))

        text.should(have.text(onboarding.text_on_page[page_number]))

        page_number += 1

    with allure.step(f'Open the {page_number} onboarding screen'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_forward_button')).click()


def test_search():
    with allure.step('Skip welcome screen'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')).click()

    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')).type('Appium')

    with allure.step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


def test_search_and_open_article():
    with allure.step('Skip welcome screen'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')).click()

    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')).type('Appium')

    with allure.step('Open the first article on the screen'):
        browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')).first.click()

    with allure.step('Verify content in the article'):
        results = browser.element((AppiumBy.CLASS_NAME, 'android.widget.TextView'))
        results.should(have.text('Appium'))
