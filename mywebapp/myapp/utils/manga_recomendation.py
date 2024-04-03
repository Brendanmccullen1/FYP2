import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
manga_df = pd.read_csv('../datasets/manga.csv')

# Drop any rows with missing values in the columns used for recommendation
manga_df.dropna(subset=['Synopsis'], inplace=True)

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(manga_df['Synopsis'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the manga that matches the title
    idx = manga_df.index[manga_df['Title'] == title].tolist()[0]

    # Get the pairwise similarity scores of all manga with that manga
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the manga based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 most similar manga (excluding the manga itself)
    sim_scores = sim_scores[1:9]

    # Get the manga indices
    manga_indices = [i[0] for i in sim_scores]

    # Return the top 9 similar manga titles
    return manga_df['Title'].iloc[manga_indices]

# Example usage
recommendations = get_recommendations('Dragon Ball')
print(recommendations)
