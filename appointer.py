import random
from selenium import webdriver
import config
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
from email.message import EmailMessage

options = Options()
options.add_experimental_option('detach', False)
options.add_argument("--disable-search-engine-choice-screen")
options.add_argument('--headless=new')
options.add_argument("--start-maximized")
options.add_argument("--window-size=3840,2160")
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)

# Get and maximise site
driver.get('https://www.stradini.lv/lv/pieteikuma-forma')
driver.maximize_window()

# Accept cookies
driver.find_element('xpath', '//button[contains(@class, "allowAll")]').click()

#Switch to iframe to work within the form
driver.switch_to.frame(driver.find_elements(By.TAG_NAME, 'iframe')[0])

#CLick Speciālisti button
specialists_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="spacialistsMainBtn"]'))
)
specialists_button.click()

#Select name from dropdown
input_field = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="SpecialistParentSearchList"]'))
)
input_field.clear()
input_field.send_keys(config.site_attributes['check_for_doctor_name'])
input_field.send_keys(Keys.RETURN)
time.sleep(random.uniform(1, 3))

#Scroll on premises button into view and click
on_premises_btn = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="onPremisesBtn"]'))
)
driver.execute_script('arguments[0].scrollIntoView(true);', on_premises_btn)
on_premises_btn.click()

#Click paidAccountBtn button
paid_visit_btn = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="paidAccountBtn"]'))
)
paid_visit_btn.click()

closest_time_div = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="colesestPaidTime"]'))
)
closest_time_string = closest_time_div.find_element(By.TAG_NAME, "b").text

print()
print(closest_time_string)

if str(config.site_attributes['send_mail_if_year']) in closest_time_string:
    server = smtplib.SMTP(config.email_config['sender_smtp_server'], config.email_config['sender_smtp_port'])
    server.starttls()
    server.login(config.email_config['sender_address'], config.email_config['sender_password'])

    msg = EmailMessage()
    msg.set_content(config.email_text['body_start'] + closest_time_string)
    msg['Subject'] = config.email_text['subject']
    msg['From'] = config.email_text['sent_from']
    msg['To'] = config.email_text['sent_to']

    server.send_message(msg)