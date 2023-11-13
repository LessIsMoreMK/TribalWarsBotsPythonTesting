import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random

class TribalWarsFarmBot:
    def tribal_wars_farm(self, farm_option, interval_min, interval_max, switch_pages):  
        
        #region Functions
        def switch_to_tab_with_url(driver, url_start):
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if driver.current_url.startswith(url_start):
                    return True
            return False
        

        def farm_using_template(driver, template, switch_pages):
            current_page = 1
            while True: 
                elements = driver.find_elements(By.CLASS_NAME, template)
                for element in elements:
                    try:
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(random.uniform(0.251, 0.3))
                        print(f"log1")
                        # Check for the error message
                        error_elements = driver.find_elements(By.XPATH, "//div[@class='autoHideBox error']/p")
                        for error_element in error_elements:
                            if 'Nie masz wystarczającej liczby jednostek' in error_element.text:
                                print("Error detected: Nie masz wystarczającej liczby jednostek")
                                return
                    
                    except Exception as e:
                        print(f"Error clicking element: {e}")

                if not switch_pages:
                    return
                current_page += 1 

                try:
                    next_page_link = driver.find_element(By.XPATH, f"//a[@class='paged-nav-item' and contains(@href, 'Farm_page={current_page - 1}')]")
                    next_page_link.click()
                except Exception:
                    print(f"Stopped at page {current_page - 1}")
                    break
        #endregion
        
        while True:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            if switch_to_tab_with_url(driver, "https://pl195.plemiona.pl/"):
                try:
                    element_to_click = driver.find_element(By.ID, "manager_icon_farm")
                    element_to_click.click()
                    farm_using_template(driver, "farm_icon_"+farm_option, switch_pages)
                except Exception as e:
                    print(f"Error interacting with the page elements: {e}")
            else:
                print("Tab with the specified URL was not found")

            
            time.sleep(random.uniform(float(interval_min), float(interval_max))*60)