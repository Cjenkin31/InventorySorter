from collections import Counter
from functools import partial

def filter_and_sort_items(items, sort_by, stat, rarity, rank, name_occurrences):
    filtered_items = [item for item in items if (rarity in [item[2], ""] and rank in [item[3], ""])]
    sort_key_func_map = {
        "Stat Total": partial(sort_key_stat_total, stat=stat),
        "Stat Amount": partial(sort_key_stat_amount, stat=stat),
        "Name": sort_key_name,
        "Rank": sort_key_rank,
        "Rarity": sort_key_rarity,
    }

    primary_sort_key_func = sort_key_func_map.get(sort_by, lambda item: 0)

    reverse = sort_by in ["Stat Total", "Stat Amount"] 

    if name_occurrences:
        name_counts = Counter(item[1] for item in filtered_items)
        filtered_items = [item for item in filtered_items if name_counts[item[1]] > 1]

    if name_occurrences or sort_by == "Name":
        # Enforce sorting by name in ascending order if duplicates are considered or sorting by name
        filtered_items.sort(key=lambda item: (item[1], primary_sort_key_func(item) if sort_by != "Name" else 0), reverse=False)
    else:
        # For other sorting criteria, use the selected sort function and reverse flag as determined
        filtered_items.sort(key=lambda item: primary_sort_key_func(item), reverse=reverse)

    return filtered_items

def sort_key_name(item):
    return item[1]

def sort_key_rank(item):
    return int(item[3])

def sort_key_rarity(item):
    return ["F", "E", "D", "C", "B", "A"].index(item[2])

def sort_key_stat_total(item, stat):
    if isinstance(item[4], dict):
        return sum(v[0] for k, v in item[4].items() if k.lower() == stat.lower())
    return 0

def sort_key_stat_amount(item, stat):
    if isinstance(item[4], dict):
        return sum(v[1] for k, v in item[4].items() if k.lower() == stat.lower())
    return 0
