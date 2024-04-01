import pandas as pd
import numpy as np
import re

# Load dataset into df_webtoon DataFrame
df_webtoon = pd.read_csv('myapp/datasets/Webtoon Dataset.csv')

# Text Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

df_webtoon['Processed_Summary'] = df_webtoon['Summary'].apply(preprocess_text)

# Create vocabulary
vocabulary = set()
for summary in df_webtoon['Processed_Summary']:
    vocabulary.update(summary.split())

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
idf_matrix = np.log(num_documents / (df_matrix + 1))

# Compute TF-IDF matrix
tfidf_matrix = tf_matrix * idf_matrix

# Compute Cosine Similarity Matrix
def compute_cosine_similarity_matrix(tfidf_matrix):
    norm_matrix = np.linalg.norm(tfidf_matrix, axis=1, keepdims=True)
    normalized_tfidf = tfidf_matrix / norm_matrix
    return np.dot(normalized_tfidf, normalized_tfidf.T)

cosine_sim_matrix = compute_cosine_similarity_matrix(tfidf_matrix)

def find_similar_webtoons(input_name, df, cosine_sim_matrix, top_n=9):
    if df.empty:
        return []

    if input_name not in df['Name'].values:
        return []

    idx = df.index[df['Name'] == input_name][0]

    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # Top N similar webtoons

    comic_indices = [i[0] for i in sim_scores]
    similar_webtoons = df.iloc[comic_indices]['Name'].tolist()

    return similar_webtoons
