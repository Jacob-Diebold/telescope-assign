from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import smtplib
import time
import datetime

import passwords


URL = passwords.URL

MY_EMAIL = passwords.MY_EMAIL
MY_PASS = passwords.MY_PASS
YOUR_EMAIL = passwords.YOUR_EMAIL


s = Service(passwords.CHROME_DIR)
op = webdriver.ChromeOptions()
# op.add_argument("--no-sandbox")
# op.add_argument('--headless')
# op.add_argument('--disable-gpu')
op.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=s, options=op)
driver.get(URL)

time.sleep(10)
username = driver.find_element("name", "email")
password = driver.find_element("name", "password")

username.send_keys(passwords.USERNAME)
password.send_keys(passwords.PASSWORD)
password.send_keys(Keys.ENTER)

number_of_scopes_xpath = '#root > div > div.sc-ksXhwv.ldhcTm > div.sc-fHYxKZ.dnKCVK > div.sc-gyUeRy.fFXEDN > div.sc-ikPAkQ.ceimHt > div'
time.sleep(30)
num_of_scopes = driver.find_element('css selector', number_of_scopes_xpath)

full_text = num_of_scopes.text
print(full_text)


split_text = full_text.split('X')

formatted_text = split_text[1]
scope_count = formatted_text.split("are")[1].split("to")[0]
driver.close()
today = datetime.datetime.today().date().strftime("%a %b %d")
with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASS)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=YOUR_EMAIL,
        msg=f"Subject: {today}-{scope_count}\n\n{formatted_text}"
    )
    print(f"Email Sent. {datetime.datetime.now()}")
