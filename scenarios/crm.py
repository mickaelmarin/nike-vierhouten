from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

class ScenarioCustom(object):
    def scenario_steps(self):
        
            liste_client = [
                "Adecco",
                "Alptis",
                "April",
                "APRR",
                "Bedrock",
                "Boccard",
                "CA-TS",
                "Groupe SEB",
                "Volvo IT",
                "AB Volvo",
                "Michelin",
                "EDF",
                "Spie",
                "Groupama",
                "G2S",
                "SNCF",
                "XPO",
                "Somfy",
                "KUEHNE + NAGEL INC",
                "FIDUCIAL",
                "GL Event",
                "Sodiaal",
                "BioMérieux",
                "Boiron",
                "Azureva",
                "Alstom",
                "Apicil",
                "Cegid",
                "Stormshield",
                "HomeServe",
                "Carrefour",
                "Sogelink",
                "Korian",
                "Mister Auto",
                "Apave",
                "ITSF",
                "Aésio",
                "Datadog"
            ]
            
            
            self.driver.get("https://app.hubspot.com/login/beta")

            time.sleep(5)
            self.driver.find_element(By.ID, "username").click()
            self.driver.find_element(By.ID, "username").send_keys("amelie.marin@smile.fr")

            self.driver.find_element(By.CSS_SELECTOR, "#loginBtn > i18n-string").click()
            time.sleep(1)
            self.driver.find_element(By.ID, "ssoBtn").click()
            time.sleep(5)

            self.driver.find_element(By.ID, "username").send_keys("ammar")
            self.driver.find_element(By.ID, "password").send_keys("Enculer32000459!")
            self.driver.find_element(By.NAME, "submit").click()
            time.sleep(5)
            self.driver.find_element(By.ID, "nav-primary-contacts-branch").click()
            self.driver.find_element(By.CSS_SELECTOR, "#nav-secondary-contacts > div").click()
            time.sleep(5)
     
            with open(".\crm.csv", "w", encoding='utf8') as f:
                for client in liste_client:
                    self.driver.find_element(By.CSS_SELECTOR, ".FilterBar__AllFiltersWrapper-xrja9u-1 i18n-string").click()
                    time.sleep(1)
                    self.driver.find_element(By.CSS_SELECTOR, 'button[data-test-id="editorAddFilterButton"]').click()
                    time.sleep(2)
                    element = self.driver.find_element(By.CSS_SELECTOR, "#crm > div:nth-child(28) > div > div > div > div > div > div > div > div.UIScrollContainer__DefaultScrollContainer-c7anuq-0.FilterEditorPanel__StyledUIScrollContainerInner-sc-1lu4eas-4.fUpjN > div > div.private-search-control.m-bottom-2 > input")
                    actions = ActionChains(self.driver)
                    actions.move_to_element(element).perform()
                    self.driver.find_element(By.CSS_SELECTOR, ".m-bottom-2 > .form-control").send_keys("Nom de l\'entreprise")
                    self.driver.find_element(By.CSS_SELECTOR, ".m-bottom-2 > .form-control").send_keys(Keys.ENTER)
                    time.sleep(1)
                    self.driver.find_element(By.CSS_SELECTOR, ".Select-input input").send_keys(client)
                    self.driver.find_element(By.CSS_SELECTOR, ".Select-input input").send_keys(Keys.ENTER)
                    time.sleep(5)
                    self.driver.find_element(By.XPATH, '//*[@id="crm"]/div[10]/div/div/div/header/div/div').click()
                    contacts_list_tab=self.driver.find_elements(By.CSS_SELECTOR, 'div[class^="IndexPage__BoardOrTableContainer"] div > div > div > div[class^="StyledTableComponents"] > table > tbody > tr')
                    
                    next_page = True
                    
                    while next_page:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, '#crm > div.app > div.IndexPage__FullPageContainer-sc-1qk8t2m-0.gqqwxU > div > div.IndexPage__BoardOrTableContainer-sc-1qk8t2m-3.eOJgiF > div > div:nth-child(3) > div > nav > span.private-paginator__forward-controls > button')
                        if next_button.get_attribute('aria-disabled') == "true":
                            next_page =False
                        contacts_list_tab=self.driver.find_elements(By.CSS_SELECTOR, 'div[class^="IndexPage__BoardOrTableContainer"] div > div > div > div[class^="StyledTableComponents"] > table > tbody > tr')    
                        for child in contacts_list_tab:
                            td = child.find_elements(By.CSS_SELECTOR,'td')
                            line = ""
                            for index, t in enumerate(td):
                                if index == 1:
                                    try:
                                        line += t.find_element(By.CSS_SELECTOR, "a").get_attribute('innerText')
                                    except:
                                        line += ""
                                elif index == 2 or index == 3 or index == 4 or index == 5 or index == 6 or index == 10:
                                    try:
                                        line += ";" + t.find_element(By.CSS_SELECTOR, "div span").get_attribute('innerText')
                                    except:
                                        line += ""
                            
                            f.write(line + '\n')
                        if next_page:
                            next_button.click()
                            time.sleep(3)
                        
                    self.driver.find_element(By.CSS_SELECTOR, ".FilterBar__AllFiltersWrapper-xrja9u-1 i18n-string").click()
                    time.sleep(1)
                    self.driver.execute_script(
                        'document.body.querySelector("#crm > div:nth-child(28) > div > div > div > div > div > div > ul > li:nth-child(1) > div > div.UIFlex__StyledFlex-w516u0-0.bSXZpV.private-flex.p-top-3.p-bottom-1 > div:nth-child(2) > button:nth-child(2) > i18n-string").click()'
                        
                    )
                    time.sleep(1)
                   
                    self.driver.find_element(By.CSS_SELECTOR, ".UIDialogButton__DialogButton-soi5uy-0").click()
            
            
            self.driver.close()