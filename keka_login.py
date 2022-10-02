import time
import os
from selenium import webdriver
from pathlib import Path
#from mail import mail_send
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#from sns import msg
from os.path import join, dirname
from dotenv import load_dotenv

#Loading .env file
dotenv_path = Path('.env')
load_dotenv(dotenv_path)

KEKA_URL = os.environ.get("KEKA_URL")
EMAIL = os.environ.get("EMAIL")
PASSWORD_KEKA = os.environ.get("PASSWORD_KEKA")

print(EMAIL)

f = open("status_storage.txt", "r")
status = f.read()

# instantiate a chrome options object so you can set the size and headless preference

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# current directory
chrome_driver = os.getcwd() +"/chromedriver"
print(chrome_driver)

def keka_login():
    global f
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    print('Login Process Started: ')
    browser.get(KEKA_URL)
    print('Website Opened')
    time.sleep(5)
    LoginPath = "//button[@title='Login with Keka Password']"
    button1 = browser.find_element_by_xpath(LoginPath)
    button1.click()
    email = browser.find_element_by_xpath('//*[@id="email"]')
    email.send_keys(EMAIL)
    print('Email Entered')
    password = browser.find_element_by_xpath('//*[@id="password"]')
    password.send_keys(PASSWORD_KEKA)
    print('Password Entered')
    time.sleep(5)
    login_button = browser.find_element_by_xpath('//*[@id="login-container-center"]/div/div/form/div/div[4]/div/button[1]')
    login_button.click()
    print('Login Button Clicked')
    time.sleep(10)
    try:
        web_clockin_button = browser.find_element_by_xpath("//button[contains(text(),'Remote Clock-In')]")
        web_clockin_button.click()
        print('Clicked WebClock In')
        time.sleep(5)
        try:
            note_text_area = browser.find_element_by_xpath("//textarea[@name='reason']")
            note_text_area.send_keys("Starting now")
            print('Entered Description')
        except:
            print("Ignoring Reason")
        time.sleep(5)

        try:
            request_button = browser.find_element_by_xpath("//button[contains(text(),'Confirm')]")
            request_button.click()
            print('Clicked Request Button')
        except:
            print("Ignoring Confirm Button")
        time.sleep(15)
        print("Refreshing the Page")
        browser.refresh()
        time.sleep(5)
        try:
            logout_button = browser.find_element_by_xpath("//button[contains(text(),'Clock-out')]")
            print('Successfully clocked in')
            #mail_send(content="LoginSuccessfull",subject="Keka Login Successfull")
            #msg(Message="Keka ClockIn Successfull")

        except:
            print("Login Failed")
            #msg(Message="Keka ClockIn Failed")
            #mail_send(content="Either you are already clocked in or some other issues has happened. \n Please Check !",subject="Keka ClockIn Failed")
        f.close()
        f = open("status_storage.txt", "w")
        f.write("False")
        f.close()
        print(time.strftime("Cron Successfully ran last at: " + "%Y-%m-%d %H:%M"))
        browser.quit()
    except:
        print("Login Failed")
        #mail_send(content="Either you are already clocked in or some other issues has happened. \n Please Check !",subject="Keka ClockIn Failed")
        #msg(Message="Keka ClockIn Failed")


keka_login()
