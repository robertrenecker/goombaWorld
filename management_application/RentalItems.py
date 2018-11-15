# from main import db
#
# class RentalItem(db.Model):
#     item_id = db.Column(db.Integer, primary_key=True)
#     item_name = db.Column(db.String(15), unique=True);
#     item_cost = db.Column(db.Float)
#     item_image_url = db.Column(db.String(100))
#
#     def __init__(self,item_name, item_cost, item_image_url):
#         self.item_name = item_name
#         self.item_cost = item_cost
#         self.item_image_url = item_image_url
#
# class Snowboard(RentalItem):
#
#     def __init__(self,item_name, item_cost, item_image_url):
#         super().__init__(item_name, item_cost, item_image_url)
#         # self.item_name = item_name
#         # self.item_cost = item_cost
#         # self.item_image_url = item_image_url
