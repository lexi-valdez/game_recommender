import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def write_data(sim_array, sheet):
    """ Write the cosine/jaccard similarity matrix to Excel

    Args:
        sim_array (numpy.ndarray/list): Cosine/Jaccard similarity matrix 
        sheet (string): Name of Excel sheet to write
    """

    df = pd.DataFrame(sim_array) # convert to dataframe format

    with pd.ExcelWriter("game_data.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer: # write to Excel
        df.to_excel(writer, sheet_name=sheet)

def calculate_cosine(combined_data_col):
    """ Finds the cosine similarity between all games

    Args:
        combined_data_col (pandas.core.series.Series): Column containing concatenated attributes of each game
    """

    cv = CountVectorizer()
    matrix = cv.fit_transform(combined_data_col)  
    cos_sim = cosine_similarity(matrix)
    write_data(cos_sim, 'Cosine Similarity')

def jaccard_similarity(set1, set2):
    """ Calculates the jaccard similarity between two games

    Args:
        set1 (set): Set of attributes for game 1
        set2 (set): Set of attributes for game 2

    Returns:
        float: Jaccard score between two games
    """

    num = len(set1.intersection(set2))
    denom = len(set1.union(set2))
    jac_score = num/denom
    return jac_score

def calculate_jaccard(preprocessed_data):
    """ Finds the jaccard similarity between all games

    Args:
        preprocessed_data (pandas.core.frame.DataFrame): Dataframe containing attributes of each game
    """

    game_dict = {}
    rows = preprocessed_data.shape[0]
    cols = preprocessed_data.shape[1]
    preprocessed_data.rename(columns={'Unnamed: 0':'Title'}, inplace=True) # rename first column as Title

    # generate dict of sets, where each set contains attributes for a single game
    for i in range(rows):
        attr_list = []
        title = preprocessed_data['Title'][i]
        for j in range(1, cols - 3): # skip over game title, 1-5 ratings, and combined column
            attr = preprocessed_data.iloc[i,j]
            if pd.isnull(attr) == False:
                attr_list.append(attr)
        game_dict[title] = set(attr_list) 

    # calculate jaccard similarity for each pair of games
    i = 0 
    j = 0
    jac_sim = [[0 for a in range(rows)] for b in range(rows)] # array of jaccard similarities for all games

    for game1 in game_dict.items():
        j = 0
        for game2 in game_dict.items():
            score = jaccard_similarity(game1[1], game2[1])
            jac_sim[i][j] = score
            j += 1
        i += 1

    write_data(jac_sim, 'Jaccard Similarity')
    
if __name__ == "__main__":
    preprocessed_data = pd.read_excel('game_data.xlsx', sheet_name='Preprocessed Data')
    calculate_cosine(preprocessed_data['CombinedData'])
    calculate_jaccard(preprocessed_data)
