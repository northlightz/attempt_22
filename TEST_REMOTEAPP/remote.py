# TEST_REMOTEAPP\remote.py
from datetime import datetime
import sys

# Adding the TEST_APP directory to the Python path to import dbmain
sys.path.insert(0, 'TEST_APP/')

from dbmain import insert_into_db, create_db
create_db()
def main():
    print('This is an example app to remotely execute commands in the db code')
    POSTER = input('Enter your username: ')
    POSTTITLE = input('Enter the title of your blog: ')
    POSTCONTENT = input('Enter the content of your blog: ')

    # Use the current date for the entry
    TIMESTAMP = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    insert_into_db(POSTER, TIMESTAMP, POSTTITLE, POSTCONTENT)
    print('Data added to the database successfully.')

if __name__ == '__main__':
    main()
