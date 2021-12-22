# Recommend 3 games based on a given game title

import pandas as pd

# input_game() prompts user for a video game they want recommendations for
def input_game():
    title = 'Fallout 4'
    return title

# generate_lookups() creates two lookup dictionaries for the row index and video game title
def generate_lookups():
    game_lookup = {}
    index_lookup = {}

    game_titles = pd.read_excel('game_data.xlsx', sheet_name='Preprocessed Data')['Unnamed: 0']

    for i in range(len(game_titles)): # row index 0 corresponds to 1st game, 1 for 2nd game, etc.
        game_lookup[i] = game_titles[i]
        index_lookup[game_titles[i]] = i

    return game_lookup, index_lookup

# find_recommendations() takes an input game title and returns 3 games most similar to it
def find_recommendations(title, game_lookup, index_lookup):
    cos_sim = pd.read_excel('game_data.xlsx', sheet_name='Cosine Similarity')
    index = index_lookup.get(title) # row corresponding to the input game title
    score_list = []

    for i in range(len(cos_sim[index])): # loop through each column and create list of valid similarity scores
        score = cos_sim[index][i]
        if index != i: # ignore when similarity score = 1 (comparing game to itself)
            score_list.append((score, i))
    
    score_list.sort(reverse=True) # sort list to find highest 3 scores
    
    for i in range(3):
        game = game_lookup.get(score_list[i][1]) # lookup game by its index
        print(game)

if __name__ == "__main__":
    game_lookup, index_lookup = generate_lookups()
    title = input_game()
    find_recommendations(title, game_lookup, index_lookup)