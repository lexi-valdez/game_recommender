# Calculate cosine similarity scores between all games
# Place data into Excel

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# write_data() writes the cosine similarity matrix to Excel
def write_data(cos_sim):  
    df = pd.DataFrame(cos_sim) # convert to dataframe format

    with pd.ExcelWriter("game_data.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer: # write to Excel
        df.to_excel(writer, sheet_name='Cosine Similarity')

# calculate_similarity() finds the cosine similarity between all games
def calculate_similarity(combined_data_col):
    cv = CountVectorizer()
    matrix = cv.fit_transform(combined_data_col)  
    cos_sim = cosine_similarity(matrix)
    write_data(cos_sim)

if __name__ == "__main__":
    preprocessed_data = pd.read_excel('game_data.xlsx', sheet_name='Preprocessed Data')
    calculate_similarity(preprocessed_data['CombinedData'])
    