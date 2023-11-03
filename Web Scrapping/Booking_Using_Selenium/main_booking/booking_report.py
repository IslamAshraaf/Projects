from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import re

class BookingReport:
  def __init__(self,hotels_boxes:WebElement):
    self.hotels_boxes = hotels_boxes

  def hotel_data(self):
    collection = []
    for hotel in self.hotels_boxes:
      #Name
      hotel_name = (hotel.find_element(By.CSS_SELECTOR,'div[data-testid="title"]').text)
      #Price
      #List Contains [1,500]
      price_extract = re.findall(r'\d+',hotel.find_element(By.CSS_SELECTOR,'span[data-testid="price-and-discounted-price"]').text)
      #Join And Convert The Two Numbers
      try:
        hotel_price = int(''.join(price_extract))
      except:
        hotel_price = 0
      #Rate
      try:
        hotel_rate = float(hotel.find_element(By.CSS_SELECTOR,'div[class="a3b8729ab1 d86cee9b25"]').text)
      except:
        hotel_rate = 0.0

      collection.append([hotel_name,hotel_price,hotel_rate])
    return collection


