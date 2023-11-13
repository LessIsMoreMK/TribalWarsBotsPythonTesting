import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

class TribalWarsGatheringBot:
    def tribal_wars_gather(self, interval_min, interval_max, get_interval):  

        #region Functions
        def switch_to_tab_with_url(driver, url_start):
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if driver.current_url.startswith(url_start):
                    return True
            return False    
        

        def click_on_link(driver, link):
            try:
                quickbar_link = driver.find_element(By.XPATH, link)
                quickbar_link.click()
            except Exception as e:
                print(f"Error while trying to click on the quickbar link: {e}")


        def click_start_button_for_level(driver, level_title):
            try:
                xpath = f"//div[contains(@class, 'scavenge-option') and div[@class='title' and contains(text(), '{level_title}')]]//a[contains(@class, 'btn') and contains(@class, 'free_send_button')]"
                start_button = driver.find_element(By.XPATH, xpath)
                start_button.click()
            except NoSuchElementException as e:
                print(f"Start button for '{level_title}' not found; Skipping; {e}")   
            except Exception as e:
                print(f"Error while trying to click on the Start button for {level_title}: {e}")      


        def handle_alert(driver):
            try:
                WebDriverWait(driver, 0.5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                if 'Brak dostępnych poziomów zbieractwa' in alert.text:
                    alert.accept()  # Click the 'OK' button on the alert
            except TimeoutException:
                print("No alert appeared within the given time.")
            except Exception as e:
                print(f"Error in handling alert: {e}")


        def gather_resources_for_level(driver, level_title):
            try:
                driver.execute_script("window.scrollTo(0, 0);")
                click_on_link(driver, "//a[@class='quickbar_link' and @data-hash='ff7f32bc9ebcb7fbd53c4360adcb2611']");    
                handle_alert(driver)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                click_start_button_for_level(driver, level_title)
                time.sleep(1)
            except Exception as e:
                print(f"Error in gathering resources for {level_title}: {e}")


        def get_max_sleep_time(driver):
            countdown_elements = driver.find_elements(By.CSS_SELECTOR, ".scavenge-option .return-countdown")
            max_time = 0

            for element in countdown_elements:
                countdown_text = element.text  
                time_parts = countdown_text.split(':')
                seconds = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
                max_time = max(max_time, seconds)

            return max_time + 60  # Add one minute
                      
        #endregion
        
        while True:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            if switch_to_tab_with_url(driver, "https://pl195.plemiona.pl/"):
                try:
                    #Go to gathering page:
                    click_on_link(driver, "//a[@class='quickbar_link' and @data-hash='cc5ffd9297792b3360ffc14dba7edf5f']");    
                    time.sleep(1)
                    click_on_link(driver, "//a[contains(@href, 'screen=place') and contains(@href, 'mode=scavenge')]")
                    time.sleep(1)

                    #Gather 4 level:
                    gather_resources_for_level(driver, "Specjaliści surowcowi")
                    
                    #Gather 3 level:
                    gather_resources_for_level(driver, "Zawodowi zbieracze")

                    #Gather 2 level:
                    gather_resources_for_level(driver, "Cierpliwi ciułacze")

                    #Gather 1 level:  
                    gather_resources_for_level(driver, "Ambitni amatorzy")

                except Exception as e:
                    print(f"Error interacting with the page elements: {e}")
            else:
                print("Tab with the specified URL was not found")

            # Wait till another iteration
            if get_interval:
                time_to_sleep = get_max_sleep_time(driver)
            else:
                time_to_sleep = random.uniform(float(interval_min), float(interval_max))*60    
            
            time.sleep(time_to_sleep)