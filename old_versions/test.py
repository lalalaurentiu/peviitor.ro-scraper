
from selenium.webdriver import Safari
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import urllib.parse
import json


urls = [
    "https://career.luxoft.com",
    "https://www.profi.ro/rezultate-cautare-cariere/",
    "https://careers.endava.com",
    "http://www.adecco.ro/jobs/",
    # "https://cariere.lidl.ro/", # nu functioneaza
    "https://veeam.wd3.myworkdayjobs.com/Veeam/"
]

url = urls[4]

cokiesExpresions = ['accept', 'gdpr', "acord", "allow"]

buttons = [
    "button[contains(@*, ",
    "input[contains(@*, ",
    "a[contains(@*, ",
]



driver = Safari(executable_path='/usr/bin/safaridriver')
driver.maximize_window()

driver.get(url)
wait = WebDriverWait(driver, 10)

def clicableElement(xpath, driver):
    element = driver.find_elements(By.XPATH, f'//{xpath}')
    if element:
        return element
    
def checkCookies(regexlst, buttons, driver):
    clicableButton = []
    for regex in regexlst:
        for btn in buttons:
            if "type" in btn:
                buttonsElement = clicableElement(f'{btn}"{regex}"]', driver)
            else:
                buttonsElement = clicableElement(f'{btn}"{regex}")]', driver)
            if buttonsElement:
                clicableButton += buttonsElement

    return clicableButton
            
def check_exists_by_xpath(xpath, driver):
    try:
        btn = driver.find_element(By.XPATH, xpath)
        return btn
    except:
        return False


sleep(3)

def capitalizeWord(string):
    return string.capitalize()

allWords = cokiesExpresions + list(map(capitalizeWord, cokiesExpresions))
print(allWords)

cookies = checkCookies(allWords, buttons, driver)
try:
    for i in cookies:
        print("found cookies")
        if i:
            print(i.get_attribute("outerHTML"))
            driver.execute_script("arguments[0].click();", i)
except Exception as e:
    print(e)
    pass
sleep(3)

searchKeywords = ["search", "cautare", "find", "gaseste"]
searchAllKeywords = searchKeywords + list(map(capitalizeWord, searchKeywords))
print(searchAllKeywords)

# for i in searchAllKeywords:
#     search = check_exists_by_xpath(f"//input[contains(@placeholder, '{i}')]", driver)
#     if search:
#         print("found search")
#         print(search.get_attribute("outerHTML"))
#         search.send_keys("Romania")
#         search.send_keys(Keys.RETURN)
#         break

sleep(3)

# Bucata de cod care face click pe butoanele de submit
# nu functioneaza

try:
    button = driver.find_elements(By.XPATH, "//button[@type='submit']")

    if button:
        
        for i in button:
            if i and i.is_displayed():
                print(i.get_attribute("outerHTML"))
                driver.execute_script("arguments[0].click();", i)
                break
except Exception as e:
    print(e)
    pass

# try:
#     for keyword in ["search", "Search"]:
#         button = driver.find_element(By.XPATH, "//a[contains(@*, 'search')]")
#         print(button.get_attribute("outerHTML"))
#         if button and button.is_displayed():
#             print("found button")
#             driver.execute_script("arguments[0].click();", button)
# except Exception as e:
#     print(e)
#     pass

sleep(10)

# sleep(2)

# paginagtionslst = []

# page = 2

# while True:
#     paginations = driver.find_elements(By.XPATH, f'//*[text() = "{page}"]')
#     if paginations:
#         paginagtionslst.append(paginations[0])
#         page += 1
#     else:
#         break


# for i in paginagtionslst:
#     try:
#         driver.execute_script("arguments[0].click();", i)
#     except:
#         pass
#     sleep(2)

# job = driver.find_elements(By.XPATH, "//a[contains(@href, 'job')]")
# for i in job:
#     print(i.text.strip())
#     # with open("jobs.txt", "a") as f:
#     #     f.write(urllib.parse.unquote(i.get_attribute("href")) + "\n")
#     sleep(3)
#     # driver.back()

# sleep(5)
driver.close()


