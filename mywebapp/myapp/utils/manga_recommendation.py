import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_manga_recommendations(title):
    # Ensure manga_df is not None and contains the necessary columns
    manga_df = pd.read_csv('myapp/datasets/manga_updated.csv')
    print(manga_df.columns)
    if manga_df is None or 'Title' not in manga_df.columns or 'image_url' not in manga_df.columns:
        return "nope"

    print("Dataset loaded successfully.")

    # Drop any rows with missing values in the columns used for recommendation
    manga_df.dropna(subset=['Synopsis'], inplace=True)
    print("Rows with missing values dropped successfully.")

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(manga_df['Synopsis'])
    print("TF-IDF Vectorization completed successfully.")

    # Compute cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    print("Cosine similarity matrix computed successfully.")

    # Check if the title exists in the dataset
    if title not in manga_df['Title'].values:
        print(f"'{title}' does not exist in the dataset")
        return []

    print(f"'{title}' exists in the dataset.")

    # Get the index of the manga that matches the title
    idx = manga_df.index[manga_df['Title'] == title].tolist()[0]

    # Get the pairwise similarity scores of all manga with that manga
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the manga based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 9 most similar manga (excluding the manga itself)
    sim_scores = sim_scores[1:10]

    recommendations = []
    for idx, score in sim_scores:
        manga_title = manga_df.loc[idx, 'Title']
        image_url = manga_df.loc[idx, 'image_url']  # Assuming 'Image_URL' is the column name
        recommendations.append({'title': manga_title, 'image_url': image_url})

    return recommendations


