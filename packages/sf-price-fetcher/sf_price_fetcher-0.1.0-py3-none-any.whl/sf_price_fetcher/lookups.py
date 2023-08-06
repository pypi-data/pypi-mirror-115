"""lookups.py

Stores the results of card price lookups in an sqlite3 db.

Records the card name, the price, and the time of fetch
whenever card price data is retrieved from scryfall.

Caching is implemented by checking if the most recent lookup
for a given card name happened more recently than 24 hours ago.
"""
import sqlite3, time
import datetime
import pypaxtor

cache_expire = datetime.timedelta(hours=24) #scryfall updates card prices every 24 hours
cache_expire = datetime.timedelta(days=7)   #meh

debug = lambda *args, **kwargs: None
#debug = print

db_location = pypaxtor.get_storage_location('sf_price_fetcher')
db_file = db_location / 'lookups.db'

con = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = con.cursor()
try:
    cur.execute("""CREATE TABLE cards (name text, time timestamp, price real)""")
except sqlite3.OperationalError:
    pass # the table already exists
con.commit()
con.close()

def cache_check(card_name):
    con = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("""SELECT * FROM cards WHERE name = ? ORDER BY time""", (card_name.lower(),))
    results = cur.fetchall()
    debug(results)
    if results:
        # If there are records of lookups for this card name,
        # return the price for the most recent one.
        name, timestamp, price = results[-1]
        debug(f'lookup: cache timestamp: {timestamp}')
        now = datetime.datetime.now()
        if now - timestamp < cache_expire:
            debug('lookup: cache hit')
            con.close()
            return price

    con.close()
    return False

def add(card_name, price):
    """Adds a lookup to the database."""
    now = datetime.datetime.now()

    con = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("""INSERT INTO cards VALUES (?, ?, ?)""", (card_name.lower(), now, price))
    con.commit()
    con.close()
