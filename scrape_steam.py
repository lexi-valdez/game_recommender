# Scrape steam data
# Place data into Excel
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_test():
    """ Scrapes data from two URLs and writes the output to a .txt. file (For testing purposes only)
    """

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

    r = requests.get('https://store.steampowered.com/search/?term=')
    soup = BeautifulSoup(r.text, 'html.parser')
    filename = "scrape_test3.txt"
    with open(filename, 'w', encoding="utf-8") as fd:
        fd.write(soup.prettify())

def get_app_ids():
    """ Gets app ids from Steam

    Returns:
        [list]: List of app ids that are used to access a URL for a specific game
    """

    app_ids = []
    url = 'https://store.steampowered.com/search/?page=' # this url is used to page through all games on Steam
                                                            # follow url with a number to get a new page of games

    max_pages = 20 # loop through pages 1 - 20 (~500 games total)
    for i in range(1, max_pages + 1):
        print(i)
        r = requests.get(url + str(i)) 
        soup = BeautifulSoup(r.text, 'html.parser')

        for game in soup.find_all("a", {"class":"search_result_row ds_collapse_flag"}):
            app_ids.append(game["data-ds-appid"])

    return app_ids

def get_game_data(url):
    """ Scrapes page for relevant game attributes

    Args:
        url (str): Steam URL corresponding to a single video game

    Returns:
        (str, list[str], list[str] str, str): Tuple of attributes for a single video game
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # get game title
    title = soup.find(itemprop='name')
    if title == None: # if title not found, set to empty string
        title = ''
    else: # else get title text
        title = title.get_text()
    
    # get genres
    genre_list = ['' for i in range(3)]
    i = 0

    if soup.find(id="genresAndManufacturer") != None: # error checking if any NoneTypes are returned
        if soup.find(id="genresAndManufacturer").find("span") != None:
            genres = soup.find(id="genresAndManufacturer").find("span").find_all("a")

            for genre in genres:
                if i == 3: # allowing three genres at most
                    break
                genre_list[i] = genre.get_text()
                i += 1

    # get user-defined tags (20 per game, ignore the 1st '' tag and the 21st '+' tag)
    tag_list = ['' for i in range(20)]
    i = 0

    tags = soup.find("div", {"class":"glance_tags popular_tags"})
    if tags != None:
        for tag in tags:
            if i == 20: # only 20 tags maximum
                break
            tag_ = tag.get_text().strip()
            if tag_ != '+' and tag_ != '':
                tag_list[i] = tag_
                i += 1

    # get percentage of positive reviews and total user reviews
    review_desc = soup.find("span", {"class":"responsive_reviewdesc_short"})
    
    if review_desc == None: # no review description, set to empty string
        pos_pct = ''
        tot_rev = ''
    else: 
        review_desc = review_desc.get_text().strip() 
        pos_idx = review_desc.index('%') 
        rev_idx_start = review_desc.index('of ') + 3
        rev_idx_end = review_desc.index(')')

        pos_pct = review_desc[1:pos_idx+1] # extract percentage of positive reviews
        tot_rev = review_desc[rev_idx_start:rev_idx_end] # extract total user reviews

    return title, genre_list, tag_list, pos_pct, tot_rev

def write_data(game_dict):  
    """ Stores scraped raw data into an Excel file

    Args:
        game_dict (dict): Dictionary of game titles and attributes to be written
    """

    df = pd.DataFrame.from_dict(game_dict, orient='index') # convert to dataframe format
    df.columns = ['Genre1', 'Genre2', 'Genre3', 'Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5', 'Tag6', 'Tag7', 'Tag8', 'Tag9', 
                'Tag10', 'Tag11', 'Tag12', 'Tag13', 'Tag14', 'Tag15', 'Tag16', 'Tag17', 'Tag18', 'Tag19', 'Tag20', 'PosPercent', 'TotalReviews'] # rename dataframe columns

    with pd.ExcelWriter("game_data.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer: # write to Excel
        df.to_excel(writer, sheet_name='Raw Data')

def scrape_steam():
    """ Loops through games on Steam, extracts relevant attributes for each game, and stores data in Excel
    """

    game_dict = {}
    app_ids = get_app_ids()
    
    for i in range(len(app_ids)): # loop through each app id
        url = 'https://store.steampowered.com/app/' + app_ids[i] # get url for each game

        data = get_game_data(url)
        game_dict[data[0]] = (data[1][0], data[1][1], data[1][2], 
                                data[2][0], data[2][1], data[2][2], data[2][3], data[2][4], data[2][5], data[2][6], data[2][7], data[2][8], data[2][9], 
                                data[2][10], data[2][11], data[2][12], data[2][13], data[2][14], data[2][15], data[2][16], data[2][17], data[2][18], data[2][19], 
                                data[3], data[4]) # separate genre_list and tag_list into separate entries

    write_data(game_dict)

if __name__ == "__main__":
    #scrape_test() # testing purposes only
    scrape_steam()
