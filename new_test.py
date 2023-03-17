#
#
#
from browser_settings import configured_driver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#
from time import sleep
import pickle
#

driver = configured_driver()

def save_cookies(driver, link: str):

    # save cookies    
    driver.get(link)
    
    


try: 
    # save cookies
    save_cookies(driver, 'https://epam.com')    

    co = driver.delete_cookie('')
    print(co)

except Exception as ex:
    print(ex)

finally: 
    sleep(10)
    driver.close()
    driver.quit()
