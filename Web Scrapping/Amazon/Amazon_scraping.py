#Libraries
#---------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pickle
import pandas as pd
import numpy as np
import time
#Core Code
#-----------------------------------------------
data = {'Brand':[],'Series':[],'Package Dimensions':[],'Resolution':[],'Processor Brand':[],'Processor Type':[],
        'Processor Speed':[],'Processor Count':[],'RAM Size':[],'Hard Drive Size':[],'Hard Disk Description':[],
        'Graphics Chipset Brand':[],'Item Weight':[],'Color':[],#Technical Details
        'Availability Date':[],'Rating':[],'Number Of Ratings':[],'Price':[]
       }
#Hide Browser Window
options = Options()
# options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
browser = webdriver.Chrome(options=options)
browser.maximize_window()
#Open Website
browser.get('https://www.amazon.eg/?language=en_AE')
#Filtering Electronics 
browser.find_element(By.ID,'searchDropdownBox').click()
browser.find_element(By.CSS_SELECTOR,'option[value="search-alias=electronics"]').click()
#Search On Laptops
browser.find_element(By.ID,'twotabsearchtextbox').send_keys('laptops')
browser.find_element(By.ID,'nav-search-submit-button').click()
#Filtering Laptops To Get Rid Of Laptop Accessories
laptops = ['lenovo','hp','dell','apple','asus','acer','msi']
for _ in range(len(laptops)):
    brand_filters = browser.find_elements(By.CSS_SELECTOR,'span[class="a-size-base a-color-base"]')
    for select in brand_filters:
        if select.text.lower() in laptops:
            select.click()
            time.sleep(2)
            break
#Sort Prices
browser.find_element(By.CLASS_NAME,'a-button-inner').click()
browser.find_element(By.CSS_SELECTOR,'li[aria-labelledby="s-result-sort-select_2"]').click()
time.sleep(2)
#Total Number Of Pages
pages = int(browser.find_element(By.CSS_SELECTOR,
                                 'span[class="s-pagination-item s-pagination-disabled"]').text)
#Looping On Pages
try:
    for page,_ in zip(range(pages-1),tqdm(range(pages-1),desc='Processing',unit=' Page',ncols=100)):
        items = browser.find_elements(By.CSS_SELECTOR,'div[data-component-type="s-search-result"]')
        for item in range(len(items)):
            try:
                #Open Item In New Tab
                items[item].find_element(By.CSS_SELECTOR, 'a').send_keys(Keys.CONTROL+Keys.RETURN)
                browser.switch_to.window(browser.window_handles[-1])
                #Wait Until Details Of Laptop Appear
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'table[class="a-keyvalue prodDetTable"]'))
                )
                #Getting Data
                titles = [title.text for title in browser.find_elements(By.CSS_SELECTOR,
                                                                        'th[class="a-color-secondary a-size-base prodDetSectionEntry"]')]
                titles_data = [data_title.text for data_title in browser.find_elements(By.CSS_SELECTOR,
                                                                                       'td[class="a-size-base prodDetAttrValue"]')]
                laptop_data = dict(zip(titles,titles_data))
                #Technical Details
                for element in list(data.keys())[:14]:
                    data[element].append(laptop_data.get(element,np.nan))
                #Av.Date
                try:
                    data['Availability Date'].append(browser.find_element(By.ID,'productDetails_detailBullets_sections1').find_elements(
                        By.CSS_SELECTOR,'td[class="a-size-base prodDetAttrValue"]')[1].text)
                except:
                    data['Availability Date'].append(np.nan)
                #Reviews
                try:
                    reviews = browser.find_element(By.ID,'averageCustomerReviews').text.split('\n')
                    data['Rating'].append(reviews[0])
                    data['Number Of Ratings'].append(reviews[1].split()[0])
                except:
                    data['Rating'].append(np.nan)
                    data['Number Of Ratings'].append(np.nan)
                #Price
                try:
                    price=browser.find_element(By.CSS_SELECTOR,'span[class="a-price-whole"]').text.split(',')
                    data['Price'].append(''.join(price))
                except:
                    data['Price'].append(np.nan)
                browser.close() #Close Item Tab (Not The Main Page)
                browser.switch_to.window(browser.window_handles[0]) #Switch To Original Window
                time.sleep(2)
            except:
                browser.save_screenshot(f'Error_Item_{item}.png')
                browser.switch_to.window(browser.window_handles[0])
                continue
        #Next Page
        browser.find_element(By.CSS_SELECTOR,
                                 'a[class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').click()
        time.sleep(5) #Take 5 Sec. To Fully Load The Page (Depends On Internet Speed),"Implicity_Wait Gives Error"
    print('Done')
except Exception as e:
    #If Any Error Occurs Take A ScreenShot And Show What Is The Problem
    browser.save_screenshot('Page_Error.png')
    print(f'Error Occurs: {type(e).__name__} ,A Picture Saved With The Error Open Project File To Show Error Image')
finally:
    #Save Data To CSV File To Analyze It Later 
    pd.DataFrame(data).to_csv('Amazon_Laptops.csv')
    #Save Data Into A File To Return It In A Variable Later; data={data included}
    with open('data.pkl','wb') as file:
        pickle.dump(data,file)
    browser.close()