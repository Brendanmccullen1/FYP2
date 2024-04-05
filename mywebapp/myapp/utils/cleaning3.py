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
character_info_df = pd.read_csv("../datasets/cleaned_character_info.csv")

# Load merged_character_info.csv
merged_df = pd.read_csv("../datasets/merged_character_info.csv")

# Identify characters present in merged_df but not in character_info_df
characters_to_remove = merged_df[~merged_df['Name'].isin(character_info_df['Name'])]['Name']

# Filter out these characters from merged_df
filtered_df = merged_df[~merged_df['Name'].isin(characters_to_remove)]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv("filtered_character_info.csv", index=False)