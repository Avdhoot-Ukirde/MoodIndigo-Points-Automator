from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from names import names as names_list  # list of names
from dates import dates as dob_list  # list of dates
from phone import phone as phone_list  # list of phone numbers
from selenium.webdriver.common.keys import Keys

# Same password for all
password = "yourpassword"

# URL of the login page
url = "https://my.moodi.org/register"

# Set up the Edge driver
driver = webdriver.Edge()

# Loop to accept multiple emails from terminal input
while True:
    # Get email input from the terminal
    email = input("Enter email (or type 'exit' to stop): ").strip()
    if email.lower() == 'exit':
        break
    
    # Open the login page
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
        continue  # Skip to the next email if this fails
    
    # Wait for the email and password fields to appear
    time.sleep(2)
    
    # Find the email and password fields and enter the credentials
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password")
    
    # Enter the email from the terminal input and the fixed password
    email_field.send_keys(email)
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
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()  # Accept the alert
            print("Alert dismissed successfully!")
        except Exception as e:
            print(f"No alert found or failed to handle alert: {e}")

    except Exception as e:
        print(f"Failed to click 'Get OTP' button: {e}")
        continue

    # Now wait for OTP input in terminal
    otp = input("Enter OTP: ").strip()

    # Wait for the OTP field to appear and then enter the OTP
    try:
        otp_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "otp"))
        )
        otp_field.clear()
        otp_field.send_keys(otp)
        print("OTP entered successfully!")

        # After entering OTP, click the 'Submit' button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
        )
        submit_button.click()
        print("Clicked 'Submit' button successfully!")

    except Exception as e:
        print(f"Failed to enter OTP or click 'Submit': {e}")
        continue

    # Generate a random name from the list and autofill it in the 'Name' field
    random_name = random.choice(names_list)

    try:
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        name_field.send_keys(random_name)
        print(f"Name '{random_name}' entered successfully!")
    except Exception as e:
        print(f"Failed to enter name: {e}")
        continue

    # Wait for the user to manually enter the Date of Birth
    print("Please enter the Date of Birth in the format YYYY-MM-DD.")
    time.sleep(5)  # Allow 5 seconds for manual entry

    # Autofill the phone number from the phone_list
    random_phone = random.choice(phone_list)

    try:
        phone_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "phone"))
        )
        phone_field.send_keys(random_phone)
        print(f"Phone Number '{random_phone}' entered successfully!")
    except Exception as e:
        print(f"Failed to enter Phone Number: {e}")
        continue

    # Select state, city, college, stream, year, and referral code
    try:
        # Select state
        state_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "state"))
        )
        state_field.send_keys("Maharashtra")
        
        # Select city
        city_field = driver.find_element(By.NAME, "city")
        city_field.send_keys("Aurangabad")

        # Enter college name
        college_field = driver.find_element(By.NAME, "college")
        college_field.send_keys("csmss")

        # Select stream
        stream_field = driver.find_element(By.NAME, "stream")
        stream_field.send_keys("Engineering")

        # Select year
        year_field = driver.find_element(By.NAME, "year")
        year_field.send_keys("Second")

        # Click next button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
        )
        next_button.click()
        print("Clicked 'Next' button successfully!")

        time.sleep(1)  # Wait for 1 second

        # Click next button again
        next_button.click()
        print("Clicked 'Next' button again successfully!")

        # Enter referral code
        referral_field = driver.find_element(By.NAME, "referral")
        referral_field.send_keys("CCP51843")

        # Click Submit button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
        )
        submit_button.click()
        print("Clicked 'Submit' button successfully!")

    except Exception as e:
        print(f"Failed to fill the form: {e}")
        continue

    # Open a new window for the next entry
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

    # Wait before moving to the next email
    time.sleep(5)

# Close the browser after all operations
driver.quit()
