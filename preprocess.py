# Discretize scraped game data
# Clean and combine each row of data into new column
# Place data into Excel

import pandas as pd

def write_data(game_dict):  
    """ Writes discretized data and combined column to an Excel sheet

    Args:
        game_dict (dict): Updated dictionary of game data
    """

    df = pd.DataFrame.from_dict(game_dict, orient='index') # convert to dataframe format
    df.columns = ['Genre1', 'Genre2', 'Genre3', 'Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5', 'Tag6', 'Tag7', 'Tag8', 'Tag9', 
                'Tag10', 'Tag11', 'Tag12', 'Tag13', 'Tag14', 'Tag15', 'Tag16', 'Tag17', 'Tag18', 'Tag19', 'Tag20', 'PosPercentDiscrete', 'TotalReviewsDiscrete', 'CombinedData'] # rename dataframe columns

    with pd.ExcelWriter("game_data.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer: # write to Excel
        df.to_excel(writer, sheet_name='Preprocessed Data')

def get_rev_rankings(review_data):
    """ Gets percentile cutoffs for the TotalReviews column

    Args:
        review_data (pandas.core.series.Series): Column of TotalReviews

    Returns:
        (int, int, int, int): Tuple of cutoffs to determine each game's 1-5 rating
    """

    review_list = []

    for i in range(len(review_data)): # convert each item in Series to an integer
        if(type(review_data[i]) ) != float: #  do not append when value is nan
            review_list.append(int(review_data[i].replace(",", "")))

    review_list.sort()
    num_ranks = len(review_list)
    
    # indices of 20th, 40th, 60th, and 80th percentile 
    twentieth = round(num_ranks * 0.2) 
    fourtieth = round(num_ranks * 0.4) 
    sixtieth = round(num_ranks * 0.6)
    eightieth = round(num_ranks * 0.8)

    return (review_list[twentieth], review_list[fourtieth], review_list[sixtieth], review_list[eightieth]) # return cutoff values for each percentile

def get_pct_label(pos_pct):
    """ Helper function that discretizes the PosPercent value into its 1-5 star rating

    Args:
        pos_pct (str): Percent of positive reviews value for a game

    Returns:
        Literal[1, 2, 3, 4, 5, ''] | None: 1-5 rating for a game
    """

    if pos_pct == 'na':
        return ''
    elif int(pos_pct) <= 20:
        return 1
    elif int(pos_pct) > 20 and int(pos_pct) <= 40:
        return 2
    elif int(pos_pct) > 40 and int(pos_pct) <= 60:
        return 3
    elif int(pos_pct) > 60 and int(pos_pct) <= 80:
        return 4
    elif int(pos_pct) > 80 and int(pos_pct) <= 100:
        return 5

def get_rev_label(tot_rev, rev_rankings):
    """ Helper function that discretizes the TotalReviews column

    Args:
        tot_rev (str): Number of total reviews for a game
        rev_rankings (int, int, int, int): Tuple of cutoffs that determine each game's 1-5 rating

    Returns:
        Literal[1, 2, 3, 4, 5, ''] | None: 1-5 rating based on total review count
    """

    if type(tot_rev) != float: # ignore blank/nan values
        tot_rev = int(tot_rev.replace(",", ""))

        if tot_rev <= rev_rankings[0]: # return 1-5 popularity score based on percentile cutoffs
            return 1
        elif tot_rev > rev_rankings[0] and tot_rev <= rev_rankings[1]:
            return 2
        elif tot_rev > rev_rankings[1] and tot_rev <= rev_rankings[2]:
            return 3
        elif tot_rev > rev_rankings[2] and tot_rev <= rev_rankings[3]:
            return 4
        elif tot_rev > rev_rankings[3]:
            return 5
    else:
        return ''

def discretize():
    """ Dicretizes the PosPercent and TotalReviews columns and removes any ™ or ® symbols in game titles to simplify the recommendation process

    Returns:
        dict: Discretized dictionary of game data
    """

    game_dict = {}
    raw_data = pd.read_excel('game_data.xlsx', sheet_name='Raw Data')
    rows = raw_data.shape[0]
    raw_data.rename(columns={'Unnamed: 0':'Title'}, inplace=True) # rename first column as Title

    rev_rankings = get_rev_rankings(raw_data['TotalReviews']) # tuple that stores popularity ranking cutoffs for TotalReviews

    for i in range(rows):
        title = raw_data['Title'][i]

        if pd.isnull(title) == False: # skip empty rows
            title = title.replace(u"\u2122", '') # replace ™ or ® symbols to clean title
            title = title.replace(u"\u00ae", '') 

            game_dict[title] = []

            game_dict[title].extend([ raw_data['Genre1'][i], raw_data['Genre2'][i], raw_data['Genre3'][i], raw_data['Tag1'][i], raw_data['Tag2'][i], raw_data['Tag3'][i], raw_data['Tag4'][i],
                                    raw_data['Tag5'][i], raw_data['Tag6'][i], raw_data['Tag7'][i], raw_data['Tag8'][i], raw_data['Tag9'][i], raw_data['Tag10'][i], raw_data['Tag11'][i],
                                    raw_data['Tag12'][i], raw_data['Tag13'][i], raw_data['Tag14'][i], raw_data['Tag15'][i], raw_data['Tag16'][i], raw_data['Tag17'][i], raw_data['Tag18'][i],
                                    raw_data['Tag19'][i], raw_data['Tag20'][i] ])

            pos_pct = str(raw_data['PosPercent'][i])[:-1] # get percent and remove '%' char
            pct_label = get_pct_label(pos_pct)
            game_dict[title].append(pct_label) # append 1-5 rating 

            tot_rev = raw_data['TotalReviews'][i] 
            rev_label = get_rev_label(tot_rev, rev_rankings) 
            game_dict[title].append(rev_label) # append 1-5 popularity score
    
    return game_dict

def combine_columns(game_dict):
    """ Loops through each game, concatenates data from each of its columns, cleans the resulting data string, then adds the data string as a new entry in game_dict

    Args:
        game_dict (dict): Dictionary of discretized game data

    Returns:
        dict: Dictionary of discretized game data and CombinedData column
    """
    
    empty_games = [] # list that tracks games with no attributes
    for game in game_dict.items(): # loop through each game
        combined = ''
        title = game[0]
        
        for item in game[1]: # loop through each list of attributes
            if pd.isnull(item) == False:
                combined += str(item).replace("-", "").replace(" ", "") + ' ' # if not null, remove whitespace/hyphens and concatenate each attribute

        combined = combined.lower().strip() # clean string after all attributes are concatenated
        if combined == '': 
            empty_games.append(title) # track games with no attributes
        
        game_dict[title].append(combined) # add string to game_dict

    # remove games that do not have any attributes
    for i in range(len(empty_games)):
        game_dict.pop(empty_games[i])

    return game_dict

if __name__ == "__main__":
    game_dict = discretize() # discretize data columns
    game_dict = combine_columns(game_dict) # add combined column to game_dict
    write_data(game_dict) # write discretized data and combined column to new Excel sheet