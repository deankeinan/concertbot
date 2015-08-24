__author__ = 'DKeinan'
import logging
logging.basicConfig(filename='testing.log', filemode='w', format='%(message)s',level=logging.INFO)
import sqlite3

class SQLManager():

    def __init__(self):
        self.sql = sqlite3.connect('sql.db')
        logging.info('SQL: database loaded/created')
        self.cur = self.sql.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
        logging.info('SQL: Loaded Completed table')
        self.commit()

    def commit(self):
        self.sql.commit()

    def select_by_postID(self, postID):
        self.cur.execute('SELECT * FROM oldposts WHERE ID=?', [postID])

    def fetch_selection(self):
        return self.cur.fetchone()

    def insert_oldpost(self, postID):
        self.cur.execute('INSERT INTO oldposts VALUES(?)', [postID])
        self.commit()
