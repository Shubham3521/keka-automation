import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pathlib import Path
#from sns import msg


from os.path import join, dirname

from dotenv import load_dotenv

#Loading .env file
dotenv_path = Path('.env')
load_dotenv(dotenv_path)

KEKA_URL = os.environ.get("KEKA_URL")
EMAIL = os.environ.get("EMAIL")
PASSWORD_KEKA = os.environ.get("PASSWORD_KEKA")

#print(EMAIL)


f = open("status_storage.txt", "r")
status = f.read()

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# current directory
chrome_driver = os.getcwd() +"/chromedriver"
print(chrome_driver)

def keka_logout():
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
        web_clockin_button = browser.find_element_by_xpath("//button[contains(text(),'Clock-out')]")
        web_clockin_button.click()
        print('Clicked WebClock Out')
        time.sleep(5)
        web_clockin_button = browser.find_element_by_xpath("//button[contains(text(),'Clock-out')]")
        web_clockin_button.click()
        print('Clicked WebClock Out Verification')
        time.sleep(5)
        browser.refresh()
        time.sleep(5)        
        try:
            logout_button = browser.find_element_by_xpath("//button[contains(text(),'Remote Clock-In')]")
            print('Successfully logged Out')
            #mail_send(content="ClockoutSuccessfull",subject="Keka Clockout Successfull")
 #           msg(Message="Keka ClockOut Successfull")

        except:
            print("Clockout Failed")
            #mail_send(content="Either you are already loggedout in or some other issues has happened. \n Please Check !",subject="Keka Clockout Failed")
 #           msg(Message="Keka ClockOut Failed")


        f.close()
        f = open("status_storage.txt", "w")
        f.write("False")
        f.close()
        print(time.strftime("Cron Successfully ran last at: " + "%Y-%m-%d %H:%M"))
        browser.quit()
    except:
        print("Clockout Failed")
        #mail_send(content="Either you are already clockedout in or some other issues has happened. \n Please Check !",subject="Keka Clockout Failed")
  #      msg(Message="Keka ClockOut Failed")





keka_logout()
