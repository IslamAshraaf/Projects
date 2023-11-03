#Libraries
from main_booking.booking import Booking
from get_data import get_currency,get_location,get_check_in,get_check_out,get_no_of_adults,get_no_of_childrens,get_ages_of_childrens,get_no_of_rooms
import time

#Getting Data
cur = get_currency()
loc = get_location()
check_in_date = get_check_in()
check_out_date = get_check_out()
no_of_adults = get_no_of_adults()
no_of_childrens = get_no_of_childrens()
if no_of_childrens!= 0:
    children_ages = get_ages_of_childrens()
no_of_rooms = get_no_of_rooms()
print('Please Wait...\n')
#-------------------------------------
#Bot Launch
try:
    with Booking() as bot:
        bot.open_page()
        bot.select_currency(currency=cur)
        bot.select_location(loc)
        bot.select_dates(check_in=check_in_date,check_out=check_out_date)
        bot.select_adults_childrens_rooms(adults=no_of_adults,childrens=no_of_childrens,rooms=no_of_rooms)
        if no_of_childrens != 0:
            bot.select_children_ages(children_ages)
        bot.submit_search()
        bot.apply_filteration()
        bot.show_report()
    
except Exception as e:
    print(type(e).__name__)



