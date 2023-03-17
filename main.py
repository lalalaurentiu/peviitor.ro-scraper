from browser_settings import configured_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import urllib.parse
import json

with open("sites.json") as f:
    file = json.load(f)

    try:
        for k, v in file.items():
            cokiesExpresions = ['ookie', 'ccept', 'consent', 'olicy', 'rivacy', 'erms', 'egal', 'greement', 'gdpr' "acord"  ]
            buttons = [
                "button[@type=",
                "input[@type=",
                "button[contains(@id, ",
                "button[contains(@class, ",
                "*[contains(text(), ",
            ]

            driver = configured_driver()
            driver.maximize_window()

            driver.get(v["url"])
            wait = WebDriverWait(driver, 10)

            def clicableElement(xpath):
                element = driver.find_elements(By.XPATH, f'//{xpath}')
                if element:
                    return element[0]
                return None
                
            def checkCookies(regexlst):
                clicableButton = None
                for regex in regexlst:
                    for btn in buttons:
                        if "type" in btn:
                            clicableButton = clicableElement(f'{btn}"{regex}"]')
                        else:
                            clicableButton = clicableElement(f'{btn}"{regex}")]')
                        
                        if clicableButton:
                            try:
                                clicableButton.click()
                            except:
                                pass    
                            break
                return clicableButton
                        
            def check_exists_by_xpath(xpath):
                try:
                    driver.find_element(By.XPATH, xpath)
                except:
                    return False
                return True

            sleep(3)

            try:

                checkCookies(cokiesExpresions)
            except:
                pass

            sleep(1)


            try:
                button = driver.find_elements(By.XPATH, "//button[@type='submit']")
                driver.execute_script("arguments[0].click();", button[0])
            except:
                pass

            try:
                button = driver.find_elements(By.XPATH, "//input[@type='submit']")
                driver.execute_script("arguments[0].click();", button[0])
            except:
                pass

            try:
                button = driver.find_elements(By.XPATH, "//button[contains(@id, 'search')]")
                driver.execute_script("arguments[0].click();", button[0])
            except:
                pass

            try:
                button = driver.find_elements(By.XPATH, "//button[contains(@class, 'search')]")
                driver.execute_script("arguments[0].click();", button[0])
            except:
                pass

            sleep(2)

            jobsKeyword = ["job", "post", "recrutare", "career", ]

            buttons = ["button", "input", "a"]

            for keyword in jobsKeyword:
                for btn in buttons:
                    exist = check_exists_by_xpath(f'//{btn}[contains(text(), "{keyword}")]')
                    existUpper = check_exists_by_xpath(f'//{btn}[contains(text(), "{keyword.capitalize()}")]')
                    if exist:
                        try:
                            button = driver.find_elements(By.XPATH, f'//{btn}[contains(text(), "{keyword}")]')
                            driver.execute_script("arguments[0].click();", button[0])
                        except:
                            pass

                    if existUpper:
                        try: 
                            button = driver.find_elements(By.XPATH, f'//{btn}[contains(text(), "{keyword.capitalize()}")]')
                            driver.execute_script("arguments[0].click();", button[0])
                        except:
                            pass

            paginagtionslst = []

            page = 2

            while True:
                paginations = driver.find_elements(By.XPATH, f'//*[text() = "{page}"]')
                if paginations:
                    paginagtionslst.append(paginations[0])
                    page += 1
                else:
                    break


            for i in paginagtionslst:
                try:
                    driver.execute_script("arguments[0].click();", i)
                except:
                    pass
                sleep(2)

                job = driver.find_elements(By.XPATH, "//a[contains(@href, 'job')]")
                for i in job:
                    print(i.get_attribute("href"))
                    with open("jobs.txt", "a") as f:
                        f.write(urllib.parse.unquote(i.get_attribute("href")) + "...." + i.text.strip() +"\n")
                
                driver.back()

            sleep(5)
            driver.close()
    except:
        pass


# from bg_dev ##################################################
new_lst = []
with open("jobs.txt", "r") as f:  
    data = f.readlines()
    
    for link in data: 
        if link.startswith('http'):
            new_lst.append(link.strip())

# make regext to filter another site...
with open('job_filter.txt', 'a') as out:
    out.write('\n'.join(new_lst) + '\n')
##################################################################
