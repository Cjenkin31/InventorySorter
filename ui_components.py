import tkinter as tk
from tkinter import ttk
from functools import partial

def setup_controls(root, search_callback, update_display_callback, reset_filters_callback, upload_csv_callback, show_previous_page_callback, show_next_page_callback, sort_options, stats_options, rarity_options, rank_options, name_occurrences_var, search_query, sort_selection_change_callback):
    controls_frame = ttk.Frame(root)
    controls_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(controls_frame, text="Search by Name:").grid(row=0, column=0, sticky="w", padx=5)
    search_entry = ttk.Entry(controls_frame, textvariable=search_query)
    search_entry.grid(row=0, column=1, sticky="ew", padx=5)
    search_entry.bind("<KeyRelease>", search_callback)

    sort_combobox = ttk.Combobox(controls_frame, values=sort_options, state="readonly")
    sort_combobox.grid(row=1, column=1, sticky="ew", padx=5)
    ttk.Label(controls_frame, text="Sort by:").grid(row=1, column=0, sticky="w", padx=5)
    sort_combobox.bind("<<ComboboxSelected>>", sort_selection_change_callback)

    stat_combobox = ttk.Combobox(controls_frame, values=stats_options, state="disabled")
    stat_combobox.grid(row=2, column=1, sticky="ew", padx=5)
    ttk.Label(controls_frame, text="Stat for Total/Amount:").grid(row=2, column=0, sticky="w", padx=5)

    rarity_combobox = ttk.Combobox(controls_frame, values=rarity_options, state="disabled")
    rarity_combobox.grid(row=3, column=1, sticky="ew", padx=5)
    ttk.Label(controls_frame, text="Rarity:").grid(row=3, column=0, sticky="w", padx=5)

    rank_combobox = ttk.Combobox(controls_frame, values=rank_options, state="disabled")
    rank_combobox.grid(row=4, column=1, sticky="ew", padx=5)
    ttk.Label(controls_frame, text="Rank:").grid(row=4, column=0, sticky="w", padx=5)

    ttk.Checkbutton(controls_frame, text="Show items with duplicate names only", variable=name_occurrences_var).grid(row=5, column=0, columnspan=2, sticky="w")

    ttk.Button(controls_frame, text="Update", command=update_display_callback).grid(row=6, column=0, pady=5, padx=5)
    ttk.Button(controls_frame, text="Reset Filters", command=reset_filters_callback).grid(row=6, column=1, pady=5, padx=5)
    ttk.Button(controls_frame, text="Upload CSV", command=upload_csv_callback).grid(row=6, column=2, pady=5, padx=5)
    
    ttk.Button(controls_frame, text="Back", command=show_previous_page_callback).grid(row=7, column=0, pady=5, padx=5)
    ttk.Button(controls_frame, text="Next", command=show_next_page_callback).grid(row=7, column=2, pady=5, padx=5)

    return sort_combobox, stat_combobox, rarity_combobox, rank_combobox
