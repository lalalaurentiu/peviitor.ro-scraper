from selenium.webdriver.common.by import By

def clicableElement(xpath, driver):
    element = driver.find_elements(By.XPATH, f'//{xpath}')
    if element:
        return element
    return None
    
def checkCookies(regexlst, buttons, driver):
    clicableButton = None
    for regex in regexlst:
        for btn in buttons:
            print(btn)
            clicableButton = clicableElement(f'{btn}"{regex}"]', driver)
    return clicableButton
            
def check_exists_by_xpath(xpath, driver):
    try:
        btn = driver.find_element(By.XPATH, xpath)
        return btn
    except:
        return False