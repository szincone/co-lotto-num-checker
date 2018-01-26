#! python 3
# lotto_scrub_compare.py - scrubs winning amounts and if > 0, will return string winner

import requests, bs4
import pandas as pd
import numpy as np

# vars
nums = None
url = None
game = (str(input('You are playing powerball, megamillions, luckyforlife, lotto, cash5, or pick3?...')))

# getting numbers and game being played
def get_nums(game):
    # gets inputs as vars depending on game and returns as str
    global nums
    if game == 'powerball' or game == 'megamillions' or game == 'luckyforlife' or game == 'lotto':
        input_1 = input('Please enter your first number ')
        input_2 = input('Please enter your second number ')
        input_3 = input('Please enter your third number ')
        input_4 = input('Please enter your fourth number ')
        input_5 = input('Please enter your fifth number ')
        input_6 = input('Please enter your sixth number ')
        nums = (input_1, input_2, input_3, input_4, input_5, input_6)
    elif game == 'cash5':
        input_1 = input('Please enter your first number ')
        input_2 = input('Please enter your second number ')
        input_3 = input('Please enter your third number ')
        input_4 = input('Please enter your fourth number ')
        input_5 = input('Please enter your fifth number ')
        nums = (input_1, input_2, input_3, input_4, input_5)
    else:
        input_1 = input('Please enter your first number ')
        input_2 = input('Please enter your second number ')
        input_3 = input('Please enter your third number ')
        nums = (input_1, input_2, input_3)
    return nums
    
# getting the url depending on game
def get_url(game):
    global url
    if game == 'powerball' or game == 'megamillions' or game == 'luckyforlife' or game == 'lotto':
        url = "https://www.coloradolottery.com/en/games/check-my-numbers/?game=" + game + "&number_1=" + nums[0] + "&number_2=" + nums[1] + "&number_3=" + nums[2] + "&number_4=" + nums[3] + "&number_5=" + nums[4] + "&extra=" + nums[5] + "&timeframe=180&check="
    elif game == 'lotto':
        url = "https://www.coloradolottery.com/en/games/check-my-numbers/?game=lotto&number_1=" + nums[0] + "&number_2=" + nums[1] + "&number_3=" + nums[2] + "&number_4=" + nums[3] + "&number_5=" + nums[4] + "&number_6=" +nums[5] + "&timeframe=180&check="
    elif game == 'cash5':
        url = "https://www.coloradolottery.com/en/games/check-my-numbers/?game=cash5&number_1=" + nums[0] + "&number_2=" + nums[1] + "&number_3=" + nums[2] + "&number_4=" + nums[3] + "&number_5=" + nums[4] + "&timeframe=180&check="
    else:
        url = "https://www.coloradolottery.com/en/games/check-my-numbers/?game=pick3&number_1=" + nums[0] + "&number_2=" + nums[1] + "&number_3=" + nums[2] + "&timeframe=180&check="

# running the functions
get_nums(game)
get_url(game)

# actually going to the site
res = requests.get(url)
res.raise_for_status() # raises exception if an issue with getting the url_data

# making soup
soup = bs4.BeautifulSoup(res.text, "html.parser")

# getting column headers for our data, starting our df
column_headers = [th.getText() for th in
                  soup.findAll('tr', limit=1)[0].findAll('th')] #limit is optional arg

# clean col headers
column_headers = [item.replace('\n', '') for item in column_headers]

# getting data_rows
data_rows = soup.findAll('tr')[1:]


# getting player data(since it's coming from a matrix, you need to make a 2d list)
data = [[td.getText() for td in data_rows[i].findAll('td')]
               for i in range(len(data_rows))]

# building our data frame
df_raw = pd.DataFrame(data, columns=column_headers)

# there are some blank columns with 'none' in them, so we'll get rid of them with notnull
df_raw = df_raw[df_raw.notnull()]

# this gets rid of any NaN columns still left, uses df.dropna, arg axis=1 selects the entire columns
df_raw = df_raw.dropna(axis=1, how='any')

# gets rid of '\n' chars in the df
df_raw.replace(regex=True, inplace=True, to_replace='\n', value='')

# gets rid of '$' symbol
df_raw['You won'] = df_raw['You won'].str.replace('$','')

# df.types are all currently objects, change them using to_numeric
df_raw = df_raw.apply(pd.to_numeric, errors='ignore')

# creating a winnings variable that lets you know if you won or not
winnings = df_raw.loc[:, 'You won'].sum()
winnings = float(winnings)

# if loop to return if there is a winner
if winnings > 0:
    print('Winner')

else:
    print('Sorry, no winner')


