
from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

usr = input("enter email Id plse :")
pwd = input("enter password: ")
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.facebook.com")
print("opening is done")
sleep(1)
username_box =  driver.find_element_by_id('email')
username_box.send_keys(usr)
print(f"Username:{username_box}")
sleep(1)
password_box = driver.find_element_by_id("pass")
username_box.send_keys(usr)
print("Password done")
login_box = driver.find_element_by_id('loginbutton')
login_box.click()
a=input("press 'q' to quit, its done")
if a=='q':
    print("its done we're closing now")
    driver.quit(10)
