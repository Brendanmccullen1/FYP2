import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('../datasets/character_image_mapping.csv')

# Drop rows where Image_URL is NaN
df_cleaned = df.dropna(subset=['Image_URL'])

# Save the cleaned DataFrame back to a CSV file
df_cleaned.to_csv('character_image_mapping_cleaned.csv', index=False)

import pandas as pd

# Read the cleaned character image mapping CSV file into a DataFrame
df_cleaned = pd.read_csv('../datasets/character_image_mapping_cleaned.csv')

# Extract the list of characters with images
characters_with_images = df_cleaned['Character'].tolist()

# Read the superheroes_power_matrix.csv file into a DataFrame
df_superheroes = pd.read_csv('../datasets/superheroes_power_matrix.csv')

# Filter the superheroes DataFrame to keep only the rows with characters present in characters_with_images
df_superheroes_filtered = df_superheroes[df_superheroes['Name'].isin(characters_with_images)]

# Save the filtered DataFrame back to superheroes_power_matrix.csv
df_superheroes_filtered.to_csv('../datasets/superheroes_power_matrix_filtered.csv', index=False)
