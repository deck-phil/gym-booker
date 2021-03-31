from src.config import CHROME_DRIVER_PATH, GYM_MANAGER_URL, START_HEADLESS, PAGE_TIMEOUT
from src.local_db import LocalDB
from src.utils import is_booking_for_today

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class GymBooker:
    driver = None
    db = None

    # Helper Methods
    def go_to_page(self, page_url):
        print('Navigating to %s' % page_url)
        self.driver.get(page_url)

    def set_input_value(self, element, value):
        return self.driver.execute_script("arguments[0].setAttribute('value', '" + str(value) + "')", element)

    # Webpage Methods
    def list_current_bookings(self):
        reserved_slots = self.driver.find_element_by_class_name('reserved-slots')
        slots = reserved_slots.find_elements_by_class_name('time-slot')

        print('-- Current Bookings --')
        for slot in slots:
            print(slot.text + '\n')

        return slots and [i.text for i in slots] or []

    def select_booking_date(self, date):
        driver = self.driver
        date_select_button = driver.find_element_by_id('btn_date_select')
        webdriver.ActionChains(driver).click(date_select_button).perform()
        try:
            WebDriverWait(driver, timeout=PAGE_TIMEOUT).until(lambda d: d.find_element_by_css_selector('div#modal_dates.in'))
        except TimeoutException as e:
            raise Exception('Cannot open day list modal.')

        # Date is in format: date_2021-03-30
        date_id = 'date_%s' % date
        selected_date = driver.find_element_by_id(date_id)
        if not selected_date:
            raise Exception('Selected booking date (%s) not found.' % date)
        webdriver.ActionChains(driver).click(selected_date).perform()

    def login(self, email, password):
        driver = self.driver

        self.go_to_page(GYM_MANAGER_URL)

        login_button = WebDriverWait(driver, timeout=PAGE_TIMEOUT).until(lambda d: d.find_element_by_id('loginButton'))
        print('Page Load Complete.')

        print('Logging in...')
        email_field = driver.find_element_by_id('emailaddress')
        self.set_input_value(email_field, email)
        password_field = driver.find_element_by_id('password')
        self.set_input_value(password_field, password)
        webdriver.ActionChains(driver).click(login_button).perform()
        try:
            WebDriverWait(driver, timeout=PAGE_TIMEOUT).until(lambda d: d.find_element_by_id('logoff'))
        except TimeoutException as e:
            raise Exception('Cannot log in!')
        print('Log in success!')

    def start_script(self):
        print('Starting Script...')
        for user in self.db.list_users():
            schedule = {
                "TU": "23:30",
                "WE": "16:00",
                "SA": "13:00"
            }
            booking_date, booking_time = is_booking_for_today(schedule)
            if booking_date and booking_time:
                try:
                    print('Starting %s' % user.email)
                    self.login(user.email, user.password)
                    current_bookings = self.list_current_bookings()
                    if len(current_bookings) > 1:
                        raise Exception('Cannot book additional session.')
                    self.select_booking_date(booking_date)
                except Exception as e:
                    print('Error: %s' % e)
                    print('Error: Continuing to next user...')
                    continue
            else:
                print('Not time for booking.')

    def init(self):
        chrome_options = Options()

        if START_HEADLESS:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-extensions')

        print('Starting Database...')
        self.db = LocalDB()

        print('Starting WebDriver...')
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=chrome_options)
        self.driver.set_window_size(1920, 1080)

        self.start_script()

        print('Closing Application.')
        self.driver.quit()


if __name__ == '__main__':
    GymBooker().init()


