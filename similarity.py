# Calculate cosine similarity scores between all games
# Place data into Excel

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def write_data(cos_sim): 
    """ Writes the cosine similarity matrix to Excel

    Args:
        cos_sim (numpy.ndarray): The cosine similarity matrix to be written
    """

    df = pd.DataFrame(cos_sim) # convert to dataframe format

    with pd.ExcelWriter("game_data.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer: # write to Excel
        df.to_excel(writer, sheet_name='Cosine Similarity')

def calculate_similarity(combined_data_col):
    """ Finds the cosine similarity between all games

    Args:
        combined_data_col (pandas.core.series.Series): Column containing concatenated attributes of each game
    """

    cv = CountVectorizer()
    matrix = cv.fit_transform(combined_data_col)  
    print(type(combined_data_col))
    cos_sim = cosine_similarity(matrix)
    write_data(cos_sim)

def calculate_jaccard():
    """ Finds the jaccard similarity between all games (In Progress)
    """
    
    print(1)

if __name__ == "__main__":
    preprocessed_data = pd.read_excel('game_data.xlsx', sheet_name='Preprocessed Data')
    calculate_similarity(preprocessed_data['CombinedData'])
    