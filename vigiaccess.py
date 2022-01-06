import time
import gspread

# Importing Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

gc = gspread.service_account(filename='creds.json')

sh = gc.open('scrapetosheets').sheet1

browser = webdriver.Chrome(executable_path=r"/home/x/vigiaccess/chromedriver")

browser.get('http://www.vigiaccess.org')

wait = WebDriverWait(browser, 10)

ADRs_POPUP_LINK = (By.CLASS_NAME, 'accordion-toggle')
# types_POPUP_LINK = (By.XPATH, './/i[contains(@ng-class, "iBranchClass()")]')

for i in range(10):
    try:
        browser.find_element(By.XPATH,
            ".//*[contains(text(), 'I confirm that I have read and understood the above statements')]"
        ).click()

        browser.find_element(By.XPATH,
            ".//*[contains(text(), 'Search database')]"
        ).click()

        inputElement = browser.find_element(By.XPATH, "(//input[@type='search'])")
        inputElement.send_keys("Covid-19 vaccine")

        browser.find_element(By.XPATH,
            ".//button[contains(@ng-click, 'getDrug(drug)')]"
        ).click()

        wait.until(EC.element_to_be_clickable(ADRs_POPUP_LINK)).click()

        # wait.until(EC.element_to_be_clickable(types_POPUP_LINK)).click()

        sources = browser.find_elements(By.XPATH, "//ul[contains(@class, 'a1 ng-scope')]/li") #.get_attribute("innerHTML")
        
        for source in sources:
            name_and_number = source.find_element(By.XPATH, ".//span").text
            name_and_number_list = name_and_number.rsplit(' ', 1)

            name = name_and_number_list[0]
            number = name_and_number_list[1].replace('(', '').replace(')', '')
            
            # Output
            print("| " + name + " | " + number + " | ")
            data = { 
                'name'   : name,
                'number' : number
            }
            print(data)

            # Putting it in spread sheet

            sh.append_row([str(data['name']), int(data['number'])])

        browser.close()

    except NoSuchElementException as e:
        print('Retry in 1 second')
        time.sleep(1)