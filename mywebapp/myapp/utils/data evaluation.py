import pandas as pd

# Load the data
df = pd.read_csv("../datasets/superheroes_power_matrix.csv")

# Drop the "Name" column since we're interested only in attributes
attributes_df = df.drop(columns=['Name'])

# Calculate the sum of each attribute across all superheroes
attribute_counts = attributes_df.sum()

# Sort the attributes in descending order of frequency and get the top 20
top_20_attributes = attribute_counts.sort_values(ascending=False).head(20)

print("Top 20 most common attributes:")
print(top_20_attributes)
