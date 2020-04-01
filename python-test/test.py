import unittest
import time
import urllib3
import sys
import requests
import random
import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

web_driver_url = None
desired_cap = None


class HealthUnitTest(unittest.TestCase):

    def setUp(self):
        if args.key:
            devices = get_target_config(args.key)
            web_driver_url = devices["driver_url"].replace("{api_token}", args.key)
            desired_cap = devices["capabilities"]
            # desired_cap["headspin.capture"] = True
            print(devices["driver_url"].replace("{api_token}", args.key))
            print(devices["capabilities"])
        elif args.url and args.browser:
            web_driver_url = args.url
            desired_cap = {
                "headspin:initialScreenSize": {
                    "width": 1920,
                    "height": 1080
                 },

                #  "headspin.capture": True

            }

            desired_cap["browserName"] = args.browser
            # desired_cap = json.loads(args.cap)
            if(args.version):
                desired_cap["browserVersion"] = args.version
            print(desired_cap)
            
            

        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Remote(command_executor=web_driver_url, desired_capabilities=desired_cap)

    def test_sign_in_powerBI(self):
        driver = self.driver
        # navigate to sign in page and click slign in button
        driver.get("https://powerbi.microsoft.com/en-us/landing/signin/")
        self.assertIn("Power BI", driver.title)
        driver.find_element_by_link_text("Sign in").click()

        time.sleep(1)

        #wait for the sign in page to load and enter the credentials
        username = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, "i0116")))
        username.send_keys("scott@headspin.io")
        username.send_keys(Keys.RETURN)

        time.sleep(2)

        password = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, "i0118")))
        password.send_keys("BriSugi12!")
        driver.find_element_by_id('idSIButton9').click()

        button = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, "idSIButton9")))
        button.click()

        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'widget-title')))
        title = driver.find_element_by_class_name('widget-title').text

        # assert that the intro widget conatins 'Scott' in the title
        self.assertIn("Scott", title)

        #################################################

        driver.find_element_by_xpath("//span[text()='Favorites']").click()
        driver.find_element_by_xpath("//span[text()='Recent']").click()
        driver.find_element_by_xpath("//span[text()='Apps']").click()
        driver.find_element_by_xpath("//span[text()='Shared with me']").click()

        self.assertItemsEqual("https://app.powerbi.com/sharedwithme?noSignUpCheck=1", driver.current_url)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()


def get_automatic_config(access_token):
    #Get the automation config (to get the appium url)
    get_auto_config = "https://api-dev.headspin.io/v0/devices/automation-config"
    r = requests.get(get_auto_config, headers={'Authorization': 'Bearer {}'.format(access_token)})
    # selenium_config = r.json()
    selenium_config = json.loads(r.text)
    return selenium_config

def get_target_config(api_token):
    configs = []
    appium_configs = get_automatic_config(api_token)
    target_appium_config = None

    for device_key in appium_configs:
        configs.append(device_key)

    index = random.randint(0, len(configs))
    target_appium_config = appium_configs[configs[index]]
    return target_appium_config



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", help="api key for org")
    parser.add_argument('--url',help="weburl for selenium server")
    parser.add_argument('--browser', help="browser for host device")
    parser.add_argument('--version', help="browser version for host device")
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    sys.argv[1:] = args.unittest_args
    unittest.main()
