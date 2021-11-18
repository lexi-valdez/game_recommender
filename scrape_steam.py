# Scrape steam data
# Place data into Excel
import requests
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd

# scrape_test() scrapes data from two URLs and writes the output to a .txt file
# this is used for testing purposes to determine how to extract the game characteristics I need
def scrape_test():
    r = requests.get('https://store.steampowered.com/app/47810/Dragon_Age_Origins__Ultimate_Edition/')
    soup = BeautifulSoup(r.text, 'html.parser')
    filename = "scrape_test1.txt"
    with open(filename, 'w', encoding="utf-8") as fd:
        fd.write(soup.prettify())

    r = requests.get('https://store.steampowered.com/app/812140/Assassins_Creed_Odyssey/')
    soup = BeautifulSoup(r.text, 'html.parser')
    filename = "scrape_test2.txt"
    with open(filename, 'w', encoding="utf-8") as fd:
        fd.write(soup.prettify())

# get_game_data() takes a steam url corresponding to a single video game
# it scrapes the page for relevant characteristics that I use to calculate similarity scores
def get_game_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # get game title
    title = soup.find(itemprop='name').get_text() 

    # get genres
    genre_list = []
    for genre in soup.find(id="genresAndManufacturer").find("span").find_all("a"):
        genre_list.append(genre.get_text())

    # get user-defined tags (20 per game, ignore the 1st '' and the 21st '+')
    tag_list = []
    for tag in soup.find("div", {"class":"glance_tags popular_tags"}):
        tag_ = tag.get_text().strip()
        if tag_ != '+' and tag_ != '':
            tag_list.append(tag_)

    # get percentage of positive reviews and total user reviews
    review_desc = soup.find("span", {"class":"responsive_reviewdesc_short"}).get_text().strip() 
    pos_idx = review_desc.index('%')
    rev_idx_start = review_desc.index('of ') + 3
    rev_idx_end = review_desc.index(')')

    pos_pct = review_desc[1:pos_idx+1] # extract percentage of positive reviews
    tot_rev = review_desc[rev_idx_start:rev_idx_end] # extract total user reviews

    print(title, genre_list, tag_list, pos_pct, tot_rev)

    # return characteristics

# write_data() stores scraped data into an Excel file
# this is used for verification purposes
def write_data():  
    # pandas and xlsxwriter code here

def scrape_steam():
    # loop through all (limit??? games)
        # run get_game_data and add to dictionary
    #write_data from dict to excel


if __name__ == "__main__":
    #scrape_test()
    url = 'https://store.steampowered.com/app/47810/Dragon_Age_Origins__Ultimate_Edition/'
    get_game_data(url)

    url = 'https://store.steampowered.com/app/812140/Assassins_Creed_Odyssey/'
    get_game_data(url)