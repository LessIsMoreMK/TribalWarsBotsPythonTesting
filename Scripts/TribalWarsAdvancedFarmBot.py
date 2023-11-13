import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

class TribalWarsAdvancedFarmBot:
    def tribal_wars_advanced_farm(self, interval_min, interval_max, switch_pages):  
            
        #region Functions
        def switch_to_tab_with_url(driver, url_start):
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                if driver.current_url.startswith(url_start):
                    return True
            return False
        
        def go_to_next_page(driver, current_page):
            try:
                next_page_link = driver.find_element(By.XPATH, f"//a[@class='paged-nav-item' and contains(@href, 'Farm_page={current_page}')]")
                next_page_link.click()
                return True
            except Exception as e:
                print(f"Stopped at page {current_page}: {e}")
                return False

        def load_all_farm_rows(driver):
            try:
                farm_rows = driver.find_elements(By.XPATH, "//tr[starts-with(@id, 'village_') and contains(@class, 'report_')]")
                return farm_rows
            except Exception as e:
                print(f"Error in loading farm rows: {e}")
                return []
    

        def get_wall_value(row):
            try:
                value_td = row.find_elements(By.XPATH, ".//td[@style='text-align: center;']")[-1]
                value = value_td.text.strip()
                return value
            except Exception as e:
                print(f"Error extracting wall value: {e}")
                return None
            
        def sent_spies(driver, row):
            try:
                place_building_link = row.find_element(By.XPATH, ".//a[.//img[contains(@src, 'graphic/buildings/place.png')]]")
                place_building_link.click()

                spy_input = driver.find_element(By.ID, "unit_input_spy")
                spy_input.clear()
                spy_input.send_keys("1")  

                send_button = driver.find_element(By.XPATH, "//form[@id='command-data-form']//input[@type='submit']")
                send_button.click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "troop_confirm_submit")))
            
                confirm_submit_button = driver.find_element(By.ID, "troop_confirm_submit")
                confirm_submit_button.click()

                #Delete Report to not repeat until attack arives
                delete_reports_link = row.find_element(By.XPATH, ".//a[.//img[contains(@src, 'graphic/delete_small.png')]]")
                delete_reports_link.click()

            except Exception as e:
                print(f"Error in sending spies: {e}")


        def process_farm_row_based_on_status(driver, row):
            try:
                status_image = row.find_elements(By.TAG_NAME, "img")[1]
                image_src = status_image.get_attribute("src")

                if "graphic/dots/green.png" in image_src:
                    handle_full_win(driver, row)
                elif "graphic/dots/blue.png" in image_src:
                    handle_scout(driver, row)
                elif "graphic/dots/red.png" in image_src or "graphic/dots/yellow.png" in image_src:
                    handle_defeat(driver, row)
                else:
                    print("Unrecognized status, skipping row.")
                 
                time.sleep(random.uniform(0.251, 0.27))   
            except Exception as e:
                print(f"Error processing farm row: {e}")



        def sent_rams(driver, row, wall_level, units_sent, units_lost):
            time.sleep(0.3)
            place_building_link = row.find_element(By.XPATH, ".//a[.//img[contains(@src, 'graphic/buildings/place.png')]]")
            place_building_link.click()
            time.sleep(0.3)


            spy_input = driver.find_element(By.ID, "unit_input_spy")
            spy_input.clear()
            spy_input.send_keys("1")  
            

            send_button = driver.find_element(By.XPATH, "//form[@id='command-data-form']//input[@type='submit']")
            send_button.click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "troop_confirm_submit")))
        
            confirm_submit_button = driver.find_element(By.ID, "troop_confirm_submit")
            confirm_submit_button.click()

            #Delete Report to not repeat until attack arives
            delete_reports_link = row.find_element(By.XPATH, ".//a[.//img[contains(@src, 'graphic/delete_small.png')]]")
            delete_reports_link.click()
           




        def handle_wall_demolition(driver, row):
            pass
            # report_link = row.find_element(By.XPATH, ".//td/a[contains(@href, 'screen=report')]").get_attribute("href")
            # driver.execute_script("window.open(arguments[0]);", report_link)
            # driver.switch_to.window(driver.window_handles[-1])
            # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "attack_info_att")))

            # units_sent = {}
            # units_lost = {}

            # # Extracting units sent
            # units_sent_elements = driver.find_elements(By.CSS_SELECTOR, "#attack_info_def_units .unit-item")
            # for element in units_sent_elements:
            #     unit_type = element.get_attribute("class").split(' ')[-1].split('-')[-1]
            #     units_sent[unit_type] = element.text

            # # Extracting units lost (if available)
            # units_lost_elements = driver.find_elements(By.CSS_SELECTOR, "#attack_info_def_units .unit-item.lost")
            # for element in units_lost_elements:
            #     unit_type = element.get_attribute("class").split(' ')[-2].split('-')[-1]
            #     units_lost[unit_type] = element.text

            # driver.close()
            # driver.switch_to.window(driver.window_handles[0])

            # wall_level = get_wall_value(row)
            # sent_rams(driver, row, wall_level, units_sent, units_lost)


        def handle_full_win(driver, row):
            numeric_value = get_wall_value(row)
            if numeric_value == "?" or numeric_value == "0":
                farm_icon_b = row.find_element(By.CLASS_NAME, "farm_icon_b")
                driver.execute_script("arguments[0].click();", farm_icon_b)
                return
            else:
                handle_wall_demolition(driver, row)
                pass
            pass



        def handle_scout(driver, row):
            handle_wall_demolition(driver, row)

        def handle_defeat(driver, row):
            try:
                report_link = row.find_element(By.XPATH, ".//td/a[contains(@href, 'screen=report')]").get_attribute("href")
                driver.execute_script("window.open(arguments[0]);", report_link)
                driver.switch_to.window(driver.window_handles[-1])
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "attack_info_att")))
                spies_sent = driver.find_element(By.CSS_SELECTOR, "td.unit-item.unit-item-spy").text
                spies_lost = driver.find_element(By.CSS_SELECTOR, "td.unit-item.unit-item-spy").text
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                if spies_sent == "0" and spies_lost == "0":
                    sent_spies(driver, row)
                else:
                    #Left the row for user handling
                    return

            except Exception as e:
                print(f"Error handling defeat: {e}")


        
        #endregion
        
        while True:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
           

            if switch_to_tab_with_url(driver, "https://pl195.plemiona.pl/"):
                try:
                    element_to_click = driver.find_element(By.ID, "manager_icon_farm")
                    element_to_click.click()
                    current_page = 1

                    while True:
                        farm_rows = load_all_farm_rows(driver)

                        for row in farm_rows:
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", row)
                            process_farm_row_based_on_status(driver, row)

                        if not switch_pages or not go_to_next_page(driver, current_page):
                            break
                        current_page += 1

                except Exception as e:
                    print(f"Error interacting with the page elements: {e}")
            else:
                print("Tab with the specified URL was not found")

            
            time.sleep(random.uniform(float(interval_min), float(interval_max))*60)
