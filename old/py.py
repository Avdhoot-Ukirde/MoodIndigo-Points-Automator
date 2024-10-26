import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Initialize API and Selenium
API_KEY = "f7SJjqmtnM1jQ+RPsAGOl5EE3g5vfNXRmLWrkv4w3RbkFjdwJPhDwy8V9rHq4SMB"
GET_EMAIL_URL = "https://api.gettestmail.com/api/v1/create"

# Email and password
password = "yourpassword"
url = "https://my.moodi.org/register"

# Random names, DOBs, and phone numbers
names_list = ["John Doe", "Jane Smith", "Alex Johnson"]
dob_list = ["1990-01-01", "1992-05-12", "1994-08-23"]
phone_list = ["9876543210", "9123456789", "9988776655"]

# Set up Selenium WebDriver
driver = webdriver.Edge()

try:
    # Generate a temporary email and open the registration page
    temp_email, email_id = generate_temp_email()
    print(f"Generated Email: {temp_email}")

    driver.get(url)
    
    # Click on 'Email Login'
    email_login_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "email_login"))
    )
    email_login_div.click()

    # Fill in email and password fields
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password")
    email_field.send_keys(temp_email)
    password_field.send_keys(password)

    # Click 'Get OTP' button
    get_otp_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Get OTP')]"))
    )
    get_otp_button.click()

    # Fetch OTP from the GetTestMail API
    def get_otp(email_id):
        otp_url = f"https://api.gettestmail.com/api/v1/emails/{email_id}"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        while True:
            response = requests.get(otp_url, headers=headers)
            if response.status_code == 200 and response.json():
                email_content = response.json()[0]
                otp = email_content["body"].split("OTP: ")[1].strip()[:6]
                return otp
            time.sleep(3)  # Wait and retry

    otp = get_otp(email_id)
    print(f"Received OTP: {otp}")

    # Enter OTP and submit
    otp_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "otp"))
    )
    otp_field.send_keys(otp)

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
    )
    submit_button.click()

    # Autofill other fields (Name, DOB, Phone, etc.)
    random_name = random.choice(names_list)
    name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "name"))
    )
    name_field.send_keys(random_name)

    random_dob = random.choice(dob_list)
    dob_field = driver.find_element(By.NAME, "dob")
    driver.execute_script("arguments[0].value = arguments[1];", dob_field, random_dob)

    random_phone = random.choice(phone_list)
    phone_field = driver.find_element(By.NAME, "phone")
    phone_field.send_keys(random_phone)

    # Select gender and click 'Next'
    gender_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "gender"))
    )
    gender_dropdown.click()
    random_gender = random.choice(["male", "female", "other"])
    gender_option = driver.find_element(By.XPATH, f"//option[@value='{random_gender}']")
    gender_option.click()

    next_button = driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
    next_button.click()
    print("Form submitted successfully!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
