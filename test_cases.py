from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    driver = webdriver.Chrome()
    driver.get("https://the-internet.herokuapp.com/login")
    return driver

def login(driver, username, password):
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button.radius")
    
    username_field.clear()
    password_field.clear()
    
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

def verify_login_success(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.success"))
        )
        print("Login successful!")
    except:
        print("Login failed!")

def verify_login_failure(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.flash.error"))
        )
        print("Login failed as expected!")
    except:
        print("Test failed: Error message not displayed!")

def test_successful_login():
    driver = setup_driver()
    login(driver, "tomsmith", "SuperSecretPassword!")
    verify_login_success(driver)
    driver.quit()

def test_incorrect_username():
    driver = setup_driver()
    login(driver, "wronguser", "SuperSecretPassword!")
    verify_login_failure(driver)
    driver.quit()

def test_incorrect_password():
    driver = setup_driver()
    login(driver, "tomsmith", "WrongPassword!")
    verify_login_failure(driver)
    driver.quit()

def test_empty_username():
    driver = setup_driver()
    login(driver, "", "SuperSecretPassword!")
    verify_login_failure(driver)
    driver.quit()

def test_empty_password():
    driver = setup_driver()
    login(driver, "tomsmith", "")
    verify_login_failure(driver)
    driver.quit()

def test_empty_username_and_password():
    driver = setup_driver()
    login(driver, "", "")
    verify_login_failure(driver)
    driver.quit()

def test_case_sensitivity():
    driver = setup_driver()
    login(driver, "TOMSMITH", "supersecretpassword!")
    verify_login_failure(driver)
    driver.quit()

def test_sql_injection():
    driver = setup_driver()
    login(driver, "admin' OR '1'='1", "password")
    verify_login_failure(driver)
    driver.quit()

# Run the tests
test_successful_login()
test_incorrect_username()
test_incorrect_password()
test_empty_username()
test_empty_password()
test_empty_username_and_password()
test_case_sensitivity()
test_sql_injection()
