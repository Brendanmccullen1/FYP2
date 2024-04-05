# import pandas as pd
# #
# # # Load the CSV file
# # df = pd.read_csv("character_info.csv")
# #
# # # Remove rows where Image_URL is missing
# # df_cleaned = df.dropna(subset=['Image_URL'])
# #
# # # Save the cleaned data to a new CSV file
# # df_cleaned.to_csv("cleaned_character_info.csv", index=False)

import pandas as pd

# Load character_info.csv
character_info_df = pd.read_csv("character_info.csv")

# Load superheroes_power_matrix.csv
superheroes_power_matrix_df = pd.read_csv("../datasets/superheroes_power_matrix.csv")

# Perform an inner merge on the "Name" column
merged_df = pd.merge(superheroes_power_matrix_df, character_info_df[['Name']], on='Name', how='inner')

# Save the result to a new CSV file
merged_df.to_csv("merged_character_info.csv", index=False)