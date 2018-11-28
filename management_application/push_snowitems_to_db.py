from main import db
import main
import pandas as pd
import os.path as path
import numpy as np
#ski_links = {'Edollo-1': 'https://www.dropbox.com/s/1k5kjvxogkalvdm/1819_Edollo-1.png?dl=0'}

def read_in_urls(df):
    for index, row in df.iterrows():
        url = row['item_url'].replace('dl=0', 'raw=1')
        #temp = main.Skis(int(row['item_id']), str(row['item_name']), float(row['item_cost']), url, int(1))
        temp = main.RentalItemFactory(int(row['item_id']), str(row['item_name']), float(row['item_cost']), url, int(1))
        temp = temp.makeSnowRental("Ski");
        try:
            db.session.add(temp)
            db.session.commit()
            print("Added %s to the database\n" % temp.getItemName())
        except:
            db.session.rollback()
            print("Failed to push items to database,\nEither because of an internal error or the item already exists in database")



#Push Snowboard Objects To Database
def read_in_snowboards(df):
    for index, row in df.iterrows():
        url = row['item_url']

        #temp = main.Skis(int(row['item_id']), str(row['item_name']), float(row['item_cost']), url, int(1))
        temp = main.RentalItemFactory(int(row['item_id']), str(row['item_name']), float(row['item_cost']), url, int(row['stock']))
        temp = temp.makeSnowRental("Snowboard");
        try:
            db.session.add(temp)
            db.session.commit()
            print("Added %s to the database\n" % temp.getItemName())
        except:
            db.session.rollback()
            print("Failed to push items to database.\n")






if __name__ == '__main__':
    base_url = path.abspath('../data/')

    print('\n\nAttempting to push new ski items to database')
    ski_objects = pd.read_csv(base_url+"/ski_item_rentals.csv", dtype={'item_id': np.dtype('int'), 'item_name': np.dtype('str'), 'item_cost':np.float64, 'item_url': np.dtype('str')})
    read_in_urls(ski_objects)

    print('\n\nAttempting to push new Snowboard items to database\n')


    snowboard_objects = pd.read_csv(base_url+"/snowboardRentals.csv")
    print("Read in snowboard objects from csv\n\n")
    read_in_snowboards(snowboard_objects)
