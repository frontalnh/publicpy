from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from threading import Semaphore
import sys
import time
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


chrome_path = ''

if sys.platform == 'darwin':
    chrome_path = 'chromedriver'
else:
    chrome_path = resource_path(
        './driver/chromedriver.exe')


class AdvancedChromeDriver(Chrome):
    def __init__(self, headless=True):
        options = ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--window-size=1400,1000")
        options.add_argument('log-level=2')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        if headless:
            options.add_argument('headless')

        # options.add_argument('--remote-debugging-port=9222')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-extensions")
        options.add_argument("disable-infobars")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # hide-console 은 콘솔창 없애려고 하는거고 service.py에서 파꿔주어야함.
        super().__init__(chrome_path, options=options,
                         service_args=["hide_console"])
        self.set_window_size(1400, 1000)
        # self.maximize_window()

    # xpath 뜰때까지 기다리고 안뜨면 패스함.
    def wait_until_xpath(self, xpath, sec=10):
        WebDriverWait(self, sec).until(EC.visibility_of_element_located(
            (By.XPATH, xpath)))

    def wait_until_xpaths(self, *xpaths):
        WebDriverWait(self, 10).until(
            EC.visibility_of_any_elements_located(
                (By.XPATH, ' | '.join(xpaths))
            )
        )

    # 이거 너무나 중요하다.
    # 클릭하기전에 무조건 있는지 기다려라 안그러면 항상 알수없는 형태의 문제가 생긴다. 최소 10초는 반드시 기다리자
    # 진심 문제의 90프로는 여기서 생기는 거였음...
    def click_xpath(self, xpath, sec=10, count=0):
        try:
            self.wait_until_xpath(xpath, sec)
            self.find_element_by_xpath(xpath).click()
        except Exception as e:
            if count > 0:
                raise e

            return self.click_xpath(xpath, sec, count+1)

    def send_keys_to_xpath(self, xpath, content, sec=10):
        self.wait_until_xpath(xpath, sec)
        self.find_element_by_xpath(xpath).clear()
        self.find_element_by_xpath(xpath).send_keys(content)

    def is_xpath_exist(self, xpath):
        return len(self.find_elements_by_xpath(xpath)) > 0

    def wait_iframe_and_switch_to_xpath(self, xpath, sec=10):
        self.wait_until_xpath(xpath)
        elem = self.find_element_by_xpath(xpath)
        WebDriverWait(self, sec).until(
            EC.frame_to_be_available_and_switch_to_it(elem))

    def wait_and_get_text(self, xpath, sec=10):
        self.wait_until_xpath(xpath, sec)
        return self.find_element_by_xpath(xpath).get_attribute('innerText')

    def wait_and_get_html(self, xpath):
        self.wait_until_xpath(xpath)
        return self.find_element_by_xpath(xpath).get_attribute('innerHTML')

    def get_html(self, xpath):
        return self.find_element_by_xpath(xpath).get_attribute('innerHTML')

    def click_xpath_until_xpath(self, clicked, shown, count=0):
        if count > 2:
            return
        try:
            self.click_xpath(clicked, 3)
            self.wait_until_xpath(shown)
        except:
            self.click_xpath_until_xpath(clicked, shown, count+1)

    def alert_exists(self, sec=10):
        try:
            WebDriverWait(self, sec).until(EC.alert_is_present())
            return True
        except:
            return False

    def wait_until_xpath_present(self, xpath, sec):
        try:
            WebDriverWait(self, sec).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
        except:
            print(self.window_handles)

    def return_to_root(self):
        time.sleep(2)
        for i, window in enumerate(self.window_handles):
            if i == 0:
                continue
            self.switch_to.window(window)
            try:
                self.close()
            except:
                # 이미 닫혔어도 노상관!
                pass

        self.switch_to.window(self.window_handles[0])

    def is_checked(self, xpath):
        return self.find_element_by_xpath(xpath).is_selected()

    def click_until_checked(self, clicked, checked, count=0):
        if count < 3 and not self.is_checked(checked):
            self.click_xpath(clicked)
            self.click_until_checked(clicked, checked, count+1)

    def is_displayed(self, xpath):
        if self.is_xpath_exist(xpath):
            return self.find_element_by_xpath(xpath).is_displayed()
        else:
            return False

    def to_last_window(self):
        self.switch_to.window(
            self.window_handles[len(self.window_handles)-1])

    def back(self):
        self.execute_script("window.history.go(-1)")

    def scroll_to_xpath(self, xpath):
        element = self.find_element_by_xpath(xpath)
        self.execute_script("arguments[0].scrollIntoView();", element)
