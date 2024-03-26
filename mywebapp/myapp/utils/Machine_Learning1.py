import pandas as pd
import numpy as np
import re

# Load dataset
df_webtoon = pd.read_csv('../datasets/Webtoon Dataset.csv', encoding='latin1')

# Text Preprocessing
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Apply preprocessing to the 'Summary' column
df_webtoon['Processed_Summary'] = df_webtoon['Summary'].apply(preprocess_text)

# Create vocabulary
vocabulary = set()
for summary in df_webtoon['Processed_Summary']:
    vocabulary.update(summary.split())

# Map each word to an index
word_to_index = {word: i for i, word in enumerate(vocabulary)}
index_to_word = {i: word for word, i in word_to_index.items()}

# Compute term frequency (TF)
tf_matrix = np.zeros((len(df_webtoon), len(vocabulary)))
for i, summary in enumerate(df_webtoon['Processed_Summary']):
    words = summary.split()
    for word in words:
        word_index = word_to_index[word]
        tf_matrix[i, word_index] += 1

# Compute document frequency (DF)
df_matrix = np.sum(tf_matrix > 0, axis=0)

# Compute inverse document frequency (IDF)
num_documents = len(df_webtoon)
idf_matrix = np.log(num_documents / (df_matrix + 1))  # Add 1 to avoid division by zero

# Compute TF-IDF matrix
tfidf_matrix = tf_matrix * idf_matrix

# Compute Cosine Similarity Matrix
def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    return dot_product / (norm_vector1 * norm_vector2)

cosine_sim_matrix = np.zeros((len(df_webtoon), len(df_webtoon)))
for i in range(len(df_webtoon)):
    for j in range(len(df_webtoon)):
        cosine_sim_matrix[i][j] = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])

# Recommendation Function
def get_similar_comics(title, cosine_sim_matrix, titles):
    if title not in titles.values:
        print(f"Comic '{title}' not found.")
        return []
    idx = titles[titles == title].index[0]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar comics
    comic_indices = [i[0] for i in sim_scores]
    return df_webtoon.iloc[comic_indices]['Name']

# Example: Get similar comics to a given comic title
similar_comics = get_similar_comics('The Nuna at Our Office', cosine_sim_matrix, df_webtoon['Name'])
print(similar_comics)
