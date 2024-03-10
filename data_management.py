import os
import csv

def find_inventory_file():
    filenames = os.listdir()
    for file in filenames:
        if file.endswith("inventory.csv"):
            return file
    return ""

def parse_stats(stats_str):
    if isinstance(stats_str, dict):
        return stats_str
    stats_dict = {}
    for stat in stats_str.split(', '):
        key, value = stat.split(':')
        stats_dict[key] = (int(value), stats_dict.get(key, (0, 0))[1] + 1)
    return stats_dict

def load_items(file_path):
    items = []
    if file_path and os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as inventory_file:
            reader = csv.reader(inventory_file)
            next(reader, None)  # Skip header
            for row in reader:
                row[4] = parse_stats(row[4])
                row[6] = row[6] or '0'
                items.append(row)
    else:
        print("No inventory CSV file found. Starting with an empty inventory.")
    return items
