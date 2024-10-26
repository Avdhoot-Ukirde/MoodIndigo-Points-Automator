from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Same password for all
password = "yourpassword"

# URL of the login page
url = "https://my.moodi.org/register"

# URL for the temp mail service
temp_mail_url = "https://tempmail.email/"

# List of random names
names_list = ["John Doe", "Jane Smith", "Alex Johnson", "Emily Davis", "Michael Brown"]

# Set up the Edge driver
driver = webdriver.Edge()

# Step 1: Fetch a temporary email address
driver.get(temp_mail_url)
time.sleep(3)

try:
    # Wait for the email to be generated and fetch it from the field or copy button
    temp_email_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='copy]"))  # Adjust the element selector based on the page
    )
    temp_email = temp_email_element.get_attribute('value')  # Get the email address value
    print(f"Temporary email fetched: {temp_email}")
except Exception as e:
    print(f"Failed to fetch temp email: {e}")
    driver.quit()
    exit()

# Step 2: Navigate to the target website and fill in the registration form with the temp email
driver.get(url)

# Wait for the 'Email Login' div to be clickable and click it
try:
    email_login_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "email_login"))
    )
    email_login_div.click()
    print("Email Login clicked successfully!")
except Exception as e:
    print(f"Failed to click 'Email Login': {e}")
    driver.quit()
    exit()

# Wait for the email and password fields to appear
time.sleep(2)

# Find the email and password fields and enter the credentials
email_field = driver.find_element(By.NAME, "email")
password_field = driver.find_element(By.NAME, "password")

# Enter the temp email and the fixed password
email_field.send_keys(temp_email)
password_field.send_keys(password)

# Click the 'Get OTP' button
try:
    get_otp_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Get OTP')]"))
    )
    get_otp_button.click()
    print("Clicked 'Get OTP' button successfully!")
    
    # Handle unexpected alert popup
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())  # Wait for the alert to appear
        alert = driver.switch_to.alert
        print(f"Alert detected: {alert.text}")
        alert.accept()  # Accept or dismiss the alert
        print("Alert dismissed successfully!")
    except Exception as e:
        print(f"No alert found or failed to handle alert: {e}")

except Exception as e:
    print(f"Failed to click 'Get OTP' button: {e}")
    driver.quit()
    exit()

# Step 3: Fetch the OTP from the temporary email
driver.get(temp_mail_url)  # Go back to temp mail site to check for the OTP
time.sleep(5)  # Wait for the email to arrive

try:
    # Look for the OTP email (this might require waiting for the email to arrive)
    otp_email_element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]/td[1]"))  # Adjust this selector to find the first email in the inbox
    )
    otp_email_element.click()  # Click on the email to open it
    time.sleep(3)
    
    # Extract the OTP from the email body (adjust this selector as per the actual page)
    otp_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'OTP')]"))  # Look for a pattern that contains OTP
    )
    otp_text = otp_element.text
    otp = ''.join(filter(str.isdigit, otp_text))  # Extract the digits from the text
    print(f"OTP fetched: {otp}")

except Exception as e:
    print(f"Failed to fetch OTP: {e}")
    driver.quit()
    exit()

# Step 4: Enter the OTP and continue the registration process
driver.get(url)  # Navigate back to the registration page

try:
    otp_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "otp"))
    )
    otp_field.send_keys(otp)
    print("OTP entered successfully!")

    # Click the 'Submit' button
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
    )
    submit_button.click()
    print("Clicked 'Submit' button successfully!")
    
except Exception as e:
    print(f"Failed to enter OTP or click 'Submit': {e}")
    driver.quit()
    exit()

# Step 5: Enter a random name from the list
random_name = random.choice(names_list)
try:
    name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "name"))
    )
    name_field.send_keys(random_name)
    print(f"Name '{random_name}' entered successfully!")
except Exception as e:
    print(f"Failed to enter name: {e}")

# Close the browser after all operations
driver.quit()
