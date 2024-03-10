class Paginator:
    def __init__(self, items, items_per_page=10):
        self.items = items
        self.items_per_page = items_per_page
        self.total_pages = max(1, len(items) // items_per_page + (1 if len(items) % items_per_page > 0 else 0))
        self.current_page = 0

    def get_current_page_items(self):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        return self.items[start:end]

    def go_to_page(self, page):
        if 0 <= page < self.total_pages:
            self.current_page = page
            return self.get_current_page_items()
        return []

    def next_page(self):
        return self.go_to_page(self.current_page + 1)

    def prev_page(self):
        return self.go_to_page(self.current_page - 1)