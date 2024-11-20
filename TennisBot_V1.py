from datetime import datetime, timedelta
from threading import Timer
import sys
from datetime import datetime
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys 
from selenium import webdriver
import time

def load_site(res_number,num,cp):
    if(cp): site_url = "https://www.nycgovparks.org/tennisreservation/reservecp/"
    else: site_url = "https://www.nycgovparks.org/tennisreservation/reserve/"
    driver.get(site_url + res_number)
    sportime_error = "We're sorry, but this time slot is not bookable anymore, please try a different time slot."
    mccarren_error = "Sorry, this field is not bookable. Please try selecting another field."
    if (driver.find_element(By.CLASS_NAME,"alert")==sportime_error or driver.find_element(By.CLASS_NAME,"alert")==mccarren_error):
        print("Reservation is Booked")
        num +=1
        if(num==6):
            sys.exit()
        else:
            load_site(str(int(res_number)+308),num,cp)
            
def click_confirm_res():
    #Go to personal info screen
    for element in range(0,34):
        ActionChains(driver)\
        .send_keys(Keys.TAB)\
        .perform()
    #35 tabs
    ActionChains(driver).send_keys(Keys.ENTER).perform()

def fill_personal_info_cp():
    #fill name,address form
    WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "num_players_2")))    
    
    #add name and permit info
    try:
        driver.find_element(By.ID,"num_players_2").click()
        driver.find_element(By.ID,"permit-number1").send_keys('#Permit Number#')
        driver.find_element(By.ID,"name1").send_keys('Name')
        driver.find_element(By.ID,"email").send_keys('Email')
        driver.find_element(By.ID,"address").send_keys('Address')
        driver.find_element(By.ID,"city").send_keys('City')
        driver.find_element(By.ID,"zip").send_keys('Zip')
        driver.find_element(By.ID,"phone").send_keys('Phone')

    except:
        print("fail filling personal info")

def fill_personal_info_mccarren():
    #fill name,address form
    WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "num_players_2")))   

    try:
        driver.find_element(By.ID,"num_players_2").click()
        driver.find_element(By.ID,"single_play_exist_2").click()
        driver.find_element(By.ID,"name").send_keys('Name')
        driver.find_element(By.ID,"email").send_keys('Email')
        driver.find_element(By.ID,"address").send_keys('Address')
        driver.find_element(By.ID,"city").send_keys('City')
        driver.find_element(By.ID,"zip").send_keys('Zip')
        driver.find_element(By.ID,"phone").send_keys('Phone')

    except:
        print("fail filling personal info")


def get_to_pay_screen():

    #control click
    time.sleep(5)
    pyautogui.rightClick(850, 600)

    for element in range(0,8):
        pyautogui.press('down')

    pyautogui.press('enter')
    pyautogui.press('enter')

def fill_cc():
    #fill cc info form
    WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "cc_number"))
    )    
    try:
        driver.find_element(By.ID,"cc_number").send_keys('#CC#')
        driver.find_element(By.ID,"expdate_month").send_keys('#Month#')
        driver.find_element(By.ID,"expdate_year").send_keys('#Date#')
        driver.find_element(By.ID,"cvv2_number").send_keys('#CCV#')
    except:
        print("fail filling CC info")

def do_booking():
    print("in booking")

    #Input reservation number
    res = 628418

    #If reservation is in Central Park
    cp = False 

    load_site(str(res), 0,cp)
    click_confirm_res()
    if(cp):fill_personal_info_cp()
    else:fill_personal_info_mccarren()
    
    #Go to payment screen
    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
     
    get_to_pay_screen()
    fill_cc()
    
    #Click pay button
    ActionChains(driver).send_keys(Keys.ENTER).perform()

def timer(secs):
    t = Timer(secs, do_booking)
    t.start()

    while(secs>30):
        time.sleep(10)
        secs-=10
        print(secs)

x=datetime.today()
y = x.replace(day=x.day+1, hour=00, minute=00, second=2, microsecond=0) + timedelta(days=1)
delta_t=y-x

secs=delta_t.seconds+1

profile_path = "/Users/username/Downloads/geckodriver"
options=Options()
options.set_preference('profile', profile_path)
#driver = webdriver.Firefox(executable_path=profile_path, options=options)
driver = webdriver.Firefox(options=options)

timer(secs)