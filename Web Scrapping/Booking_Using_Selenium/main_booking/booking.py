import main_booking.constants as const
from main_booking.booking_filteration import BookFilteration
from main_booking.booking_report import BookingReport
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from prettytable import PrettyTable
import time
import csv

class Booking(webdriver.Edge):
    
    def __init__(self,shutdown=False):
        self.shutdown = shutdown
        # Ignoring The Devtools Messages in CMD
        options = Options()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        super(Booking,self).__init__(options=options)
        self.maximize_window()
        self.implicitly_wait(10)
        
    def open_page(self):
        self.get(const.url)
        self.find_element(By.CSS_SELECTOR,"button[aria-label='Dismiss sign-in info.']").click()

    def select_currency(self,currency='EGP'):
        
        self.find_element(By.CSS_SELECTOR,'button[data-testid="header-currency-picker-trigger"]').click()
        buttons = self.find_elements(By.CSS_SELECTOR,"button[data-testid='selection-item']")
        for button in buttons:
            if "ea1163d21f e8e856c3e0" in button.find_element(By.CSS_SELECTOR,"span[class='cf67405157']").find_element(By.TAG_NAME,"div").get_attribute('class') and currency == button.find_element(By.CSS_SELECTOR,"span[class='cf67405157']").find_element(By.TAG_NAME,"div").text:
                button.click()
                break
            else: 
                if currency == button.find_element(By.CSS_SELECTOR,"span[class='cf67405157']").find_element(By.TAG_NAME,"div").text:
                    button.click()
                    break
        
    def select_location(self,location):
        self.implicitly_wait(10)
        search_bar  = self.find_element(By.NAME,'ss')
        search_bar.clear()
        search_bar.send_keys(location)
        time.sleep(2)
        #Clicking on the first element in search
        self.find_element(By.CSS_SELECTOR,"li[id='autocomplete-result-0']").click()

    def select_dates(self,check_in,check_out):
        #Click On Check In
        self.find_element(By.CSS_SELECTOR,f"span[data-date='{check_in}']").click()
        #Click on check out
        self.find_element(By.CSS_SELECTOR,f"span[data-date='{check_out}']").click()

    def select_adults_childrens_rooms(self,adults=1,childrens=0,rooms=1):
        self.find_element(By.CSS_SELECTOR,"button[data-testid='occupancy-config']").click()
        #List that contains index: 
        # 0-->No. of Adults 
        # 1 -->No. of Childrens
        # 2--> No. of Rooms
        adl_chi_rm = self.find_elements(By.CSS_SELECTOR,"div[class='bfb38641b0']")

        #Formate selecting adults
        while int(adl_chi_rm[0].find_element(By.CLASS_NAME,'d723d73d5f').text) != 1:
            adl_chi_rm[0].find_elements(By.TAG_NAME,'button')[0].click()
        #Select no. of adults
        while int(adl_chi_rm[0].find_element(By.CLASS_NAME,'d723d73d5f').text) != adults:
            adl_chi_rm[0].find_elements(By.TAG_NAME,'button')[1].click()

        #Select no. of childrens
        while int(adl_chi_rm[1].find_element(By.CLASS_NAME,'d723d73d5f').text) != childrens:
            adl_chi_rm[1].find_elements(By.TAG_NAME,'button')[1].click()

        #Selectin No. of Rooms
        while int(adl_chi_rm[2].find_element(By.CLASS_NAME,'d723d73d5f').text) != rooms:
            adl_chi_rm[2].find_elements(By.TAG_NAME,'button')[1].click()
        
    def select_children_ages(self,ages:list=None):    
        #Selecting Ages Of Childs
        ages_list = self.find_elements(By.NAME,'age')
        for select in ages_list:
            select.click()
            options = select.find_elements(By.TAG_NAME,'option')
            for option in options:
                if ages[ages_list.index(select)] == int(option.get_attribute('value')):
                    option.click()
                    break

    def submit_search(self):
        self.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

    def apply_filteration(self):
        self.implicitly_wait(10)
        filteration = BookFilteration(driver=self)
        filteration.star_rating(4,5)
        filteration.sort_price()

    def show_report(self):
        self.implicitly_wait(10)
        hotels = self.find_elements(By.CSS_SELECTOR,'div[data-testid="property-card"]')
        report = BookingReport(hotels)
        #Getting Collection of Hotels
        collections = report.hotel_data()
        table = PrettyTable(['Name','Price','Rate'])
        table.add_rows(collections)
        print(table)
        #Getting The Current Currency
        currency = self.find_element(By.CSS_SELECTOR,'span[class="e4adce92df"]').text
        #Importing To CSV
        with open('Hotels.csv','w',newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name',
                             f'Price({currency})',
                             'Rate'])
            writer.writerows(collections)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.shutdown:
            self.quit()
    
    
