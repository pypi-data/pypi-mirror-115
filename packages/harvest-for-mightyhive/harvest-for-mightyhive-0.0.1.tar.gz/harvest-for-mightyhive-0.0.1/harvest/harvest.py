"""
Note:

1. Resume timer needs some improvement. When there are multiple
items, it does not know which task's time to start.

2. Login should use harvest build-in login method, not google SSO.

"""
import time
from datetime import date, datetime

from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import NoSuchElementException


class Harvest:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self._login()

    def _login(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get("https://id.getharvest.com/harvest/sign_in")
        driver.find_element_by_xpath('//*[@id="email"]')\
              .send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="password"]')\
              .send_keys(self.password)
        driver.find_element_by_xpath('//*[@id="log-in"]').click()
        return driver

    @property
    def date(self):
        if "day" not in self.driver.current_url:
            return date.today()

        info = self.driver.current_url.split("/")
        year, month, day = int(info[-4]), int(info[-3]), int(info[-2])
        return date(year, month, day)

    @date.setter
    def date(self, value: date):
        url = (
            "https://mhsfdc.harvestapp.com/time/day/"
            f"{value.year}/{value.month}/{value.day}/3790451"
        )
        entry_xpath = '//*[@id="main"]/div[2]/div/section/div[1]/div[1]/button'
        self.driver.get(url)
        self.driver.find_element_by_xpath(entry_xpath).click()

    @property
    def project(self):
        xpath = '//*[@id="calendar-recurring-event-popover-wrapper"]/div[2]/div/a/span' # noqa
        return self.driver.find_element_by_xpath(xpath).text

    @project.setter
    def project(self, value):
        xpath = '//*[@id="calendar-recurring-event-popover-wrapper"]/div[2]/div/a' # noqa
        self.driver.find_element_by_xpath(xpath).click()
        self.driver \
            .find_element_by_css_selector(f'li[title="{value}"]') \
            .click()

    @property
    def task(self):
        xpath = '/html/body/div[3]/div[1]/div[1]/form/div[2]/div/a/span'
        return self.driver.find_element_by_xpath(xpath).text

    @task.setter
    def task(self, value):
        xpath = '/html/body/div[3]/div[1]/div[1]/form/div[2]/div/a'
        self.driver.find_element_by_xpath(xpath).click()
        self.driver \
            .find_element_by_css_selector(f'li[title="{value}"]') \
            .click()

    @property
    def note(self):
        return

    @note.setter
    def note(self, text):
        self.driver.find_element_by_name("notes").send_keys(text)

    @property
    def duration(self):
        return self.driver.find_element_by_name("hours").get_attribute("value")

    @duration.setter
    def duration(self, value: datetime):
        """
        format: X:X  or  X.X
        """
        self.driver.find_element_by_name("hours").send_keys(value)

    def submit(self):
        xpath = "/html/body/div[3]/div[1]/div[1]/form/div[4]/button[1]"
        elem = self.driver.find_element_by_xpath(xpath)
        if elem.text != "Save Entry":
            raise ValueError("Please specify duration.")
        elem.click()

    def start_timer(self):
        xpath = "/html/body/div[3]/div[1]/div[1]/form/div[4]/button[1]"
        elem = self.driver.find_element_by_xpath(xpath)
        if elem.text != "Start Timer":
            raise ValueError("Please do not specify duration.")
        elem.click()
        self.driver.close()

    def stop_timer(self):
        try:
            self.driver.close()
        except InvalidSessionIdException:
            pass
        self.driver = self._login()
        time.sleep(2)
        selector = 'button[data-analytics-element-id="timesheet-stop-timer"]'
        try:
            self.driver \
                .find_element_by_css_selector(selector) \
                .click()
        except NoSuchElementException:
            raise ValueError("No timer to stop.")

    def resume_timer(self):
        try:
            self.driver.close()
        except InvalidSessionIdException:
            pass
        self.driver = self._login()
        time.sleep(2)
        selector = 'button[data-analytics-element-id="timesheet-start-timer"]'
        try:
            self.driver \
                .find_element_by_css_selector(selector) \
                .click()
        except NoSuchElementException:
            raise ValueError("No timer to resume.")
