from datetime import datetime
from main_booking.constants import months,avaliable_currencies
from prettytable import PrettyTable

def get_currency():
  print('Available Currencies','\n','*'*20)
  table = PrettyTable(['Currency','Name'])
  table.add_rows(avaliable_currencies)
  print(table)
  print('Hint : Write The Name Of Currency As Shown In (Name) Column')
  
  while True:
    currency = input('Enter Currency : ').upper()
    found=False
    for cur in avaliable_currencies:
      if cur[1].strip() == currency:
        found=True
        return currency
    if found==True:
      break
    else:
      print('Invalid Currency')
  
def get_location():
  while True:
    loc = input('Enter Location You Want To Go: ').capitalize()
    if loc.isdigit():
      print('Invalid Location')
    else:
      return loc

def get_check_in():
  global check_in_year,check_in_month,check_in_day
  #Get check in year
  while True:
    check_in_year = input('Enter Check In Year : ')
    if check_in_year.isdigit():
      check_in_year = int(check_in_year)
      if check_in_year in range(datetime.now().year,datetime.now().year+2):
        break
      else:
          print('Invalid Year Range')
    else:
      print('Invalid Type')

  #Get check in month
  while True:
    check_in_month = input('Enter Check In Month : ')
    if check_in_month.isdigit():
      check_in_month = int(check_in_month)
      if check_in_year == datetime.now().year and check_in_month in range(datetime.now().month,13):
        break
      elif check_in_year != datetime.now().year and check_in_month in range(1,13):
        break
      else:
        print('Invalid Month Range')
    else:
      print('Invalid Type')
  #Get check in day
  while True:
    check_in_day = input('Enter Check In Day : ')
    if check_in_day.isdigit():
      check_in_day = int(check_in_day)

      if check_in_year==datetime.now().year and check_in_month==datetime.now().month and check_in_day in range(datetime.now().day+1,months[check_in_month]+1):
        break
      elif check_in_year==datetime.now().year and check_in_month!=datetime.now().month and check_in_day in range(1,months[check_in_month]+1):
        break
      elif check_in_year!=datetime.now().year and check_in_day in range(1,months[check_in_month]+1):
        break
      else:
        print('Invalid Day')
    else:
      print('Invalid Type')

  if check_in_month in range(1,10):
    check_in_month = f'0{check_in_month}'
  if check_in_day in range(1,10):
    check_in_day = f'0{check_in_day}'

  return f'{check_in_year}-{check_in_month}-{check_in_day}'
  
def get_check_out():
  global check_in_year,check_in_month,check_in_day
  if isinstance(check_in_month,str):
    check_in_month = int(check_in_month[1])
  if isinstance(check_in_day,str):
    check_in_day = int(check_in_day[1])
  #Get check out year
  while True:
    check_out_year = input('Enter Check Out Year : ')
    if check_out_year.isdigit():
      check_out_year = int(check_out_year)
      if check_out_year in range(datetime.now().year,datetime.now().year+2):
        break
      else:
          print('Invalid Year Range')
    else:
      print('Invalid Type')

  #Get check out month
  while True:
    check_out_month = input('Enter Check Out Month : ')
    if check_out_month.isdigit():
      check_out_month = int(check_out_month)
      if check_out_year == check_in_year and check_out_month>=check_in_month and check_out_month in range(1,13):
        break
      elif check_out_year != check_in_year and check_out_month in range(1,13):
        break
      else:
        print('Invalid Month')
    else:
      print('Invalid Type')
  #Get check in day
  while True:
    check_out_day = input('Enter Check Out Day : ')
    if check_out_day.isdigit():
      check_out_day = int(check_out_day)

      if check_out_year==check_in_year and check_out_month==check_in_month and check_out_day>check_in_day and check_out_day in range(1,months[check_out_month]+1):
        break
      elif check_out_year==check_in_year and check_out_month>check_in_month and check_out_day in range(1,months[check_out_month]+1):
        break
      elif check_out_year!=check_in_year and check_in_day in range(1,months[check_out_month]+1):
        break
      else:
        print('Invalid Day')
    else:
      print('Invalid Type')

  if check_out_month in range(1,10):
    check_out_month = f'0{check_out_month}'
  if check_out_day in range(1,10):
    check_out_day = f'0{check_out_day}'

  return f'{check_out_year}-{check_out_month}-{check_out_day}'

def get_no_of_adults():
  while True:
    no_of_adults = input('Enter Number Of Adults : ')
    if no_of_adults.isdigit():
      no_of_adults = int(no_of_adults)
      if no_of_adults in range(1,31):
        break
    else:
      print('Invalid Type Or Range Of Adults\n (Max Limit=30)')
  return no_of_adults
  
def get_no_of_childrens():
  global no_of_childrens
  while True:
    no_of_childrens = input('Enter Number Of Childrens : ')
    if no_of_childrens.isdigit():
      no_of_childrens = int(no_of_childrens)
      if no_of_childrens in range(0,11):
        break
    else:
      print('Invalid Type Or Limit Of Child\n (Max Limit Is = 10)')
  return no_of_childrens

def get_ages_of_childrens():
  global no_of_childrens
  ages = []
  for age in range(no_of_childrens):
    while True:
      child_age = input(f'Enter Age Of Child {age+1} : ')
      if child_age.isdigit():
        child_age = int(child_age)
        if child_age in range(0,18):
          ages.append(child_age)
          break
      else:
        print('Invalid Type Or Age Of Child')
  return ages

def get_no_of_rooms():
  while True:
    no_of_rooms = input('Enter Number Of Rooms : ')
    if no_of_rooms.isdigit():
      no_of_rooms = int(no_of_rooms)
      if no_of_rooms in range(1,31): 
        break
    else:
      print('Invalid Type Or Limit Of Child\n (Max Limit Is = 30)')
  return no_of_rooms
