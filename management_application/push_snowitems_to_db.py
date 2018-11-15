from main import db
import main
import pandas as pd
import os.path as path
import numpy as np
#ski_links = {'Edollo-1': 'https://www.dropbox.com/s/1k5kjvxogkalvdm/1819_Edollo-1.png?dl=0'}

def read_in_urls(df):
    for index, row in df.iterrows():
        url = row['item_url'].replace('dl=0', 'raw=1')
        temp = main.Skis(int(row['item_id']), str(row['item_name']), float(row['item_cost']), url, int(1))
        try:
            db.session.add(temp)
            db.session.commit()
            print("Added %s to the database\n" % temp.item_name)
        except:
            db.session.rollback()
            print("Failed to push items to database,\nEither because of an internal error or the item already exists in database")


if __name__ == '__main__':
    base_url = path.abspath('../../data/ski_item_rentals.csv')

    print('\n\nAttempting to push new ski items to database')
    ski_objects = pd.read_csv(base_url, dtype={'item_id': np.dtype('int'), 'item_name': np.dtype('str'), 'item_cost':np.float64, 'item_url': np.dtype('str')})
    read_in_urls(ski_objects)
