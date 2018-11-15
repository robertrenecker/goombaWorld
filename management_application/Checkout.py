
class Checkout():
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(item):
        self.items.append(item)

    def remove_items(item):
        self.items.remove(item)

    def get_number_of_items():
        return len(self.items)

    def get_total_of_cart():
        self.total = 0
        for item in items:
            self.total += item.item_cost
        return ("Total of cart is: %f" % self.total)
