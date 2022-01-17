# Video Game Recommender
This program web scrapes ~500 video games from Steam and calculates the similarity scores between them.
When the user is looking for a new game to play, they can enter a video game they enjoyed into the recommender. This program then returns 3 similar games that the user can play next.

This Video Game Recommender is written in Python and uses the Requests, BeautifulSoup, Pandas, Sklearn, and Tkinter libraries. 

## Motivation
I decided to work on a recommendation system since it would encapsulate the entire data science process from start to finish. I had previous experience with exploratory data analysis in Python, but did not have much exposure to data collection and cleaning. This project allowed me to pre-process the data myself and apply common data science algorithms that I had not used before. I chose video games specifically since I mainly play RPGs and thought this would be useful the next time I run out of games to play.

## Process

The Video Game Recommender has four steps:
1. Web Scrape Data (scrape_steam.py)
2. Preprocess Data (preprocess.py)
3. Calculate Similarity (similarity.py)
4. Recommend Games (recommend_cosine.py, recommend_jaccard.py)

### Step 1: Web Scrape Data
To scrape data from Steam, I started at the following URL: https://store.steampowered.com/search/.
This URL lists all products sold on Steam. I went through the first 22 pages of this list and extracted the App ID for each video game.

Each video game in Steam has its own URL where game data is displayed. Every URL starts with "https://store.steampowered.com/app/" and is followed by the game's App ID. Using the list of App ID's I generated earlier, I visited each game's URL and grabbed key attributes. These attributes included the game's title, genre (up to 3), user-defined tags (up to 20), percentage of positive reviews, and the total number of reviews.

See the "Raw Data" sheet in game_data.xlsx for my results.

### Step 2: Preprocess Data
To apply cosine/jaccard similarity, I had to make sure all of my data was discrete. This meant transforming the numerical "PosPercent" and "TotalReviews" columns into a 1 to 5 categorical rating. 

For the "PosPercent" column, values of 0%-20% were assigned a 1 rating, 21%-40% were a 2, 41%-60% were a 3, 61-80% were a 4, and 81-100% were a 5. 

For the "TotalReviews" column, I partitioned the values into 5 equal groups, where a 1 corresponded with the lowest 20% of values, 2 was the lowest 21%-40% of values, 3 was 41%-60%, 4 was 61%-80%, and 5 was 81%-100%. For example, if I had the "TotalReviews" values 1000, 2000, 2500, 3500, 4000, 5000, 5500, 6000, 8000, 8500 the corresponding 1-5 rating would be 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, respectively.

After discretizing, I added the "CombinedData" column. This column cleaned and concatenated all of the attributes for each game, which was needed to calculate the cosine similarities.

I also removed empty rows, as well as the symbols ™ and ® from game titles.

See the "Preprocessed Data" sheet in game_data.xlsx for my results.

### Step 3: Calculate Similarity
To calculate the Cosine similarity, I used CountVectorizer's fit_transform() on the "CombinedData" column to count how many times each attribute appeared in a particular video game. I then called Sklearn's cosine_similarity() to return an array of cosine similarities between all games.

To calculate the Jaccard similarity, I put each game's attributes into a set. I omitted the "PosPercentDiscrete" and "TotalReviewsDiscrete" columns since the 1-5 ratings would not have much meaning on their own. For example, Game A could have PosPercentDiscrete = 4 and TotalReviewsDiscrete = 5 while Game B could have the values switched. When calculating the set intersection for Game A and Game B, the algorithm would include both 4 and 5 in the intersection, even though the 4 and 5 values mean something completely different between Game A and Game B.

See the "Cosine Similarity" and "Jaccard Similarity" sheets in game_data.xlsx for my results. Note that each row/col corresponds to the same row in "Preprocessed Data" For example, Row 2 in "Preprocessed Data" is "God of War". Row 2 and Column 2 in "Cosine Similarity" (Cell B2) corresponds to the cosine similarity between "God of War" and itself. Row 3 Column 2 (Cell B3) corresponds to the similarity between "God of War" and "Counter-Strike: Global Offensive."

### Step 4: Recommend Games 
I split recommend_cosine.py and recommend_jaccard.py into two separate files so that I could run the files side-by-side and compare.

Both scripts use Tkinter to prompt the user for a video game title. When the user clicks "Enter," the program finds the Excel row in "Cosine Similarity" or "Jaccard Similarity" that corresponds to the user's input title. It then finds the three highest similarity scores within that row and returns the corresponding video game titles in order.

## Results
A few of my results for the Cosine (left) and Jaccard (right) recommenders are below. There were a few variations between the two recommenders but they returned at least two of the same game titles.

![Skyrim Result](/results/Skyrim_Result.png)
![Fifa Result](/results/Fifa_Result.png)
![Mass Effect Result](/results/Mass_Effect_Result.png)
![Black Ops Result](/results/Black_Ops_Result.png)

This program also returns "None" if the user tries to enter a game that doesn't exist in the data.

![Error Result](/results/Error_Result.png)

## Resources
- scrape_steam.py
    - https://andrew-muller.medium.com/scraping-steam-user-reviews-9a43f9e38c92 
- preprocess.py, recommend_cosine,py, recommend_jaccard.py
    - https://www.datacamp.com/community/tutorials/recommender-systems-python
    - https://medium.com/web-mining-is688-spring-2021/netflix-movies-and-tv-shows-recommender-using-cosine-similarity-e053ee42a85b
    - https://towardsdatascience.com/using-cosine-similarity-to-build-a-movie-recommendation-system-ae7f20842599
    - https://www.statology.org/jaccard-similarity-python/
    - https://datatofish.com/entry-box-tkinter/