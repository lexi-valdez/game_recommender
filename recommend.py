# Recommend 3 games based on a given game title

import pandas as pd
import tkinter as tk

def generate_lookups():
    """ Creates two lookup dictionaries for the row index and video game title

    Returns:
        (dict, dict): Dictionary from row index to game title and dictionary from game title to row index
    """

    game_lookup = {}
    index_lookup = {}

    game_titles = pd.read_excel('game_data.xlsx', sheet_name='Preprocessed Data')['Unnamed: 0']

    for i in range(len(game_titles)): # row index 0 corresponds to 1st game, 1 for 2nd game, etc.
        game_lookup[i] = game_titles[i]
        index_lookup[game_titles[i]] = i

    return game_lookup, index_lookup

def handle_user():
    """ Prompts user for a video game title and displays 3 most recommended games
    """

    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=240)
    canvas.pack()

    prompt = tk.Label(root, text='Enter a video game title:') # create prompt text
    canvas.create_window(110, 30, window=prompt)

    entry = tk.Entry(root) # create input text box
    canvas.create_window(200, 60, width=300, window=entry)

    # initialize results to display later
    result1 = tk.Label(root, text='')
    canvas.create_window(200, 130, window=result1)
    result2 = tk.Label(root, text='')
    canvas.create_window(200, 160, window=result2)
    result3 = tk.Label(root, text='')
    canvas.create_window(200, 190, window=result3)

    def find_recommendations():
        """ Generates 3 games using cosine similarity scores and prints them to screen
        """
        
        game_lookup, index_lookup = generate_lookups()
        title = entry.get() # get user input title

        cos_sim = pd.read_excel('game_data.xlsx', sheet_name='Cosine Similarity')
        index = index_lookup.get(title) # row corresponding to the input game title

        if index == None: # if game does not exist in database, use default values
            game1, game2, game3 = 'None', 'None', 'None' 
        else: # otherwise, find 3 most similar games
            score_list = []
            for i in range(len(cos_sim[index])): # loop through each column and create list of valid similarity scores
                score = cos_sim[index][i]
                if index != i: # ignore when similarity score = 1 (comparing game to itself)
                    score_list.append((score, i))
        
            score_list.sort(reverse=True) # sort list to find highest 3 scores

            game1 = game_lookup.get(score_list[0][1]) # lookup first game by its index
            game2 = game_lookup.get(score_list[1][1]) # lookup second game by its index
            game3 = game_lookup.get(score_list[2][1]) # lookup third game by its index

        # show results on screen
        result1.config(text='Game 1: ' + game1)
        result2.config(text='Game 2: ' + game2)
        result3.config(text='Game 3: ' + game3)

    button = tk.Button(text='Enter', command=find_recommendations)
    canvas.create_window(200, 90, window=button)
    
    root.mainloop()

if __name__ == "__main__":
    handle_user()