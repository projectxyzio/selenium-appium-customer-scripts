import urllib3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import exceptions

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def setup(web_driver_url):
    desired_cap = {
        "headspin:initialScreenSize": {
            "width": 1920,
            "height": 1080
        },
    }
    desired_cap["browserName"] = 'chrome'

    driver = webdriver.Remote(command_executor=web_driver_url, desired_capabilities=desired_cap)
    return driver
    
class SeleniumTestException(Exception):
    pass

def do_basic_signin(driver):
    from selenium.webdriver.support.ui import WebDriverWait

    # navigate to sign in page and click slign in button
    
    driver.get("https://powerbi.microsoft.com/en-us/landing/signin/")
    

    if "Power BI" not in driver.title:
        raise SeleniumTestException("Did not find 'Power BI' in the page title '{}'".format(driver.title))

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
    password.send_keys(Keys.RETURN)

    time.sleep(2)
     
    button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.ID, "idSIButton9")))

    driver.execute_script("arguments[0].click();", button)
    # button.click()

    WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'widget-title')))
    title = driver.find_element_by_class_name('widget-title').text

    # assert that the intro widget conatins 'Scott' in the title
    # self.assertIn("Scott", title)
    if "Scott" not in title:
        raise SeleniumTestException("Could not find 'Scott' in the widget title '{}'".format(title))

    #################################################

     # favorites
    driver.find_element(By.CSS_SELECTOR, "nav-pane-expander:nth-child(2) nav-pane-button > button").click()
    # recent
    driver.find_element(By.CSS_SELECTOR, "nav-pane-expander:nth-child(3) span").click()
    # apps
    driver.find_element(By.CSS_SELECTOR, ".myApps span").click()
    # shared with me
    driver.find_element(By.CSS_SELECTOR, ".sharedWithMe span").click()

    expect_url = 'https://app.powerbi.com/sharedwithme?noSignUpCheck=1'

    if expect_url != driver.current_url:
        raise SeleniumTestException("Unexpected url '{}', expected '{}'".format(driver.current_url, expect_url))
    
    driver.quit()

def find_favorites_button(driver):
    try:
        favorites_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "nav-pane-expander:nth-child(2) nav-pane-button > button"))) 
    except:
        print("Exception Occurred")
        favorites_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//span[text()='Favorites']")))
    return favorites_button


if __name__ == "__main__":
    web_driver_url = "https://dev-us-la-0.headspin.io:9090/v0/f26664f6bfc64becac8f4c4819f4b5c2/wd/hub"
    driver = setup(web_driver_url)
    do_basic_signin(driver)
    