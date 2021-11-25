import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori

# write_data() writes discretized data to an Excel sheet
def write_data(game_dict):  
    df = pd.DataFrame.from_dict(game_dict, orient='index') # convert to dataframe format
    df.columns = ['Genre1', 'Genre2', 'Genre3', 'Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5', 'Tag6', 'Tag7', 'Tag8', 'Tag9', 
                'Tag10', 'Tag11', 'Tag12', 'Tag13', 'Tag14', 'Tag15', 'Tag16', 'Tag17', 'Tag18', 'Tag19', 'Tag20', 'PosPercentDiscrete', 'TotalReviewsDiscrete'] # rename dataframe columns

    with pd.ExcelWriter("game_data.xlsx", engine="openpyxl", mode="a") as writer: # write to Excel
        df.to_excel(writer, sheet_name='Discretized Data')

def get_rev_rankings(review_data):
    review_list = []

    for i in range(len(review_data)): # convert each item in Series to an integer
        if(type(review_data[i]) ) != float: #  do not append when value is nan
            review_list.append(int(review_data[i].replace(",", "")))

    review_list.sort()
    num_ranks = len(review_list)
    
    twentieth = round(num_ranks * 0.2)
    fourtieth = round(num_ranks * 0.4)
    sixtieth = round(num_ranks * 0.6)
    eightieth = round(num_ranks * 0.8)

    return (review_list[twentieth], review_list[fourtieth], review_list[sixtieth], review_list[eightieth])

# get_pct_label() is a helper function that discretizes the PosPercent value into its 1-5 star rating
def get_pct_label(pos_pct):
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

# get_rev_label() is a helper function that discretizes the TotalReviews value
def get_rev_label(tot_rev, rev_rankings):
    if type(tot_rev) != float: # ignore blank/nan values
        tot_rev = int(tot_rev.replace(",", ""))
        if tot_rev <= rev_rankings[0]:
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

# discretize() takes the PosPercent and TotalReviews columns and places them into discrete categories
def discretize():
    game_dict = {}
    raw_data = pd.read_excel('game_data.xlsx', sheet_name='Raw Data')
    rows = raw_data.shape[0]
    raw_data.rename(columns={'Unnamed: 0':'Title'}, inplace=True) # rename first column as Title

    rev_rankings = get_rev_rankings(raw_data['TotalReviews']) # tuple that stores popularity ranking cutoffs for TotalReviews

    for i in range(rows):
        title = raw_data['Title'][i]
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
    
    write_data(game_dict)

# preprocess_data() transforms raw game data so that it's useable by apriori
def preprocess_data():
    discretize()

    transactions = []
    data = pd.read_excel('game_data.xlsx', sheet_name='Discretized Data')    
    rows = data.shape[0]
    cols = data.shape[1]
    print(rows,cols)
    
    for i in range(rows):
       for j in range(1, 26): 
           transactions.append(str(data.values[i, j]))
    
    #print(transactions)


# run_model() runs the apriori algorithm on preprocessed game data
def run_model():
    print(1)

if __name__ == "__main__":
    preprocess_data()