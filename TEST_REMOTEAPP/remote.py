# TEST_REMOTEAPP\remote.py
import sys
import json

# Adding the TEST_APP directory to the Python path to import dbmain
sys.path.insert(0, 'TEST_APP/')

from dbmain import insert_into_db, create_db

def main():
    print('This script reads blog posts from a JSON file and adds them to the database')

    # Create the database
    create_db()

    # Read from the JSON file
    with open('blog_posts.json', 'r') as f:
        for line in f:
            post = json.loads(line.strip())

            # Insert each post into the database
            insert_into_db(post['poster'], post['timestamp'], post['title'], post['content'])
            print(f"Added post: {post['title']} by {post['poster']}")

    print('All data from the JSON file has been added to the database successfully.')

if __name__ == '__main__':
    main()