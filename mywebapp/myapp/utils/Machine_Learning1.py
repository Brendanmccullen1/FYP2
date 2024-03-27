import pandas as pd
import numpy as np
import re

# Load dataset

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
# tf_matrix = np.zeros((len(df_webtoon), len(vocabulary)))
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

def find_similar_webtoons(input_name, df, top_n=9, n_clusters=9):
    if df.empty:
        return f"The DataFrame is empty. Please make sure your CSV file contains data."

    if input_name not in df['Name'].values:
        return f"The input webtoon {input_name} was not found in the DataFrame."

    idx = df[df['Name'] == input_name].index[0]

    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # Top N similar webtoons

    comic_indices = [i[0] for i in sim_scores]
    similar_webtoons = df.iloc[comic_indices]['Name'].tolist()

    return similar_webtoons

# Example: Get similar webtoons to a given webtoon title
similar_webtoons = find_similar_webtoons('The Nuna at Our Office', df_webtoon)
print(similar_webtoons)
