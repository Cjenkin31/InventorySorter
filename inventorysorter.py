import os
import re
from collections import Counter
import tkinter as tk
from tkinter import ttk
from tkinter import BooleanVar
from tkinter import filedialog
import shutil
from functools import partial
from paginator import Paginator
from data_management import find_inventory_file, load_items, parse_stats
from ui_components import setup_controls
from item_filters import filter_and_sort_items

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Items")
        root.geometry("400x600")

        # Options
        self.sort_options = ["Name", "Stat Total", "Stat Amount", "Rarity","Rank"]
        self.stats_options = ["Defense", "Dexterity", "Intelligence", "Health"]
        self.rarity_options = ["F", "E", "D", "C", "B", "A"]
        self.rank_options = [str(i) for i in range(1, 6)]

        # State variables
        self.name_occurrences_var = BooleanVar(value=False)
        self.search_query = tk.StringVar()

        # Data
        self.items = load_items(find_inventory_file())
        self.paginator = Paginator(self.items, items_per_page=4)

        # UI Setup
        self.sort_combobox, self.stat_combobox, self.rarity_combobox, self.rank_combobox = setup_controls(
            self.root, self.search_items, self.update_display, self.reset_filters, self.upload_csv, 
            self.show_previous_page, self.show_next_page, self.sort_options, self.stats_options, 
            self.rarity_options, self.rank_options, self.name_occurrences_var, self.search_query, 
            self.on_sort_selection_change)
        self.setup_items_display()

    def search_items(self, event=None):
        search_query = self.search_query.get().strip().lower()
        if search_query:
            filtered_items = [item for item in self.items if search_query in item[1].lower()]
            self.update_display(filtered_items)
        else:
            self.update_display()

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        for file in os.listdir():
            if re.search(".*inventory\.csv$", file):
                os.remove(file)

        new_file_path = "inventory.csv"

        shutil.copy(file_path, new_file_path)

        self.items = load_items(find_inventory_file())
        self.paginator = Paginator(self.items, items_per_page=4)
        self.update_display()

    def on_sort_selection_change(self, event=None):
        selected_sort_option = self.sort_combobox.get()
        # Stat options
        if selected_sort_option in ["Stat Total", "Stat Amount"]:
            self.stat_combobox['state'] = 'readonly'
        else:
            self.stat_combobox['state'] = 'disabled'
            self.stat_combobox.set('')
        # Rank option
        if selected_sort_option in ["Rank"]:
            self.rank_combobox['state'] = 'readonly'
        else:
            self.rank_combobox['state'] = 'disabled'
            self.rank_combobox.set('')
        # Rarity option
        if selected_sort_option in ["Rarity"]:
            self.rarity_combobox['state'] = 'readonly'
        else:
            self.rarity_combobox['state'] = 'disabled'
            self.rarity_combobox.set('')

    def reset_filters(self):
        self.sort_combobox.set('')
        self.stat_combobox['state'] = 'disabled'
        self.stat_combobox
        self.rarity_combobox.set('')
        self.rarity_combobox['state'] = 'disabled'
        self.rank_combobox.set('')
        self.rank_combobox['state'] = 'disabled'
        self.name_occurrences_var.set(False)
        self.update_display()

    def setup_items_display(self):
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.items_canvas = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e))
        items_canvas_id = self.canvas.create_window((0, 0), window=self.items_canvas, anchor="nw")
        self.items_canvas.bind("<Configure>", lambda e: self.on_frame_configure())

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.current_page = 0

        self.populate_items_frame()

    def update_display(self, items_to_display=None):
        if items_to_display is None:
            sort_by = self.sort_combobox.get()
            stat = self.stat_combobox.get()
            rarity = self.rarity_combobox.get()
            rank = self.rank_combobox.get()
            name_occurrences = self.name_occurrences_var.get()
            items_to_display = filter_and_sort_items(self.items, sort_by, stat, rarity, rank, name_occurrences)
            
        self.paginator = Paginator(items_to_display, items_per_page=4)
        self.populate_items_frame()

    def populate_items_frame(self, items_to_display=None):
        for widget in self.items_canvas.winfo_children():
            widget.destroy()
        if items_to_display is None:
            items_to_display = self.paginator.get_current_page_items()
        for i, item in enumerate(items_to_display):
            row = i // 2
            col = i % 2
            self.create_item_frame(item, row, col)

    def create_item_frame(self, item, row, col):
        item_frame = ttk.LabelFrame(self.items_canvas, text=f"Item {item[5]}", borderwidth=2, relief="groove", padding=(10, 10))
        if not isinstance(item[4], dict):
            item[4] = parse_stats(item[4])

        ttk.Label(item_frame, text=f"Name: {item[1]}").grid(row=1, column=0, sticky="w")
        ttk.Label(item_frame, text=f"Rarity: {item[2]}").grid(row=2, column=0, sticky="w")
        ttk.Label(item_frame, text=f"Rank: {item[3]}").grid(row=3, column=0, sticky="w")
        ttk.Label(item_frame, text="Stats:").grid(row=4, column=0, sticky="w")
        stat_row = 5
        for k, v in item[4].items():
            stat_name = k.capitalize()
            stat_value = f"    {stat_name}: {v[0]} (x{v[1]})"
            ttk.Label(item_frame, text=stat_value).grid(row=stat_row, column=0, sticky="w")
            stat_row += 1
        ttk.Label(item_frame, text=f"Attack Power: {item[6]}").grid(row=stat_row + 1, column=0, sticky="w")

        item_frame.grid(row=row, column=col, padx=10, pady=5)

    def show_previous_page(self):
        self.paginator.prev_page()
        self.populate_items_frame()

    def show_next_page(self):
        self.paginator.next_page()
        self.populate_items_frame()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure(self):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
