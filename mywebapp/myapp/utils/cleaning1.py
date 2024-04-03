import csv
import os

def remove_missing_entries():
    # Read webtoon_info.csv and identify entries with missing data
    entries_to_remove = []
    with open('../datasets/webtoon_info.csv', 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if 'not found' in row.values():
                entries_to_remove.append(row['Name'])

    # Remove entries from webtoon_info.csv
    if entries_to_remove:
        with open('../datasets/webtoon_info.csv', 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            rows_to_keep = [row for row in reader if row['Name'] not in entries_to_remove]

        with open('../datasets/webtoon_info.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_to_keep)

    # Remove corresponding entries from Webtoon Dataset.csv
    if entries_to_remove:
        with open('../datasets/Webtoon Dataset.csv', 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames

            # Identify entries to keep
            rows_to_keep = []
            for row in reader:
                if row['Name'] not in entries_to_remove:
                    rows_to_keep.append(row)

        with open('../datasets/Webtoon Dataset.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_to_keep)

    print("Entries with missing data removed successfully.")

# Call the function to remove missing entries
remove_missing_entries()
