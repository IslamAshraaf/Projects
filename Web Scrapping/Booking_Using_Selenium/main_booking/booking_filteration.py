from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time

class BookFilteration():
    def __init__(self,driver:WebDriver):
        self.driver = driver
        self.driver.implicitly_wait(10)
        
    def star_rating(self,*stars_values):
        self.driver.implicitly_wait(5)
        star_filteration_box = self.driver.find_element(By.CSS_SELECTOR,"div[data-filters-group='class']")
        star_childs = star_filteration_box.find_elements(By.CSS_SELECTOR,'*')
        for star_value in stars_values:
          for star_select in star_childs:
              if str(star_select.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                  star_select.click()
                  time.sleep(2)
                  
    def sort_price(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.CSS_SELECTOR,"button[data-testid='sorters-dropdown-trigger']").click()
        
        self.driver.find_element(By.CSS_SELECTOR,'button[data-id="price"]').click()
        time.sleep(3)
        
        