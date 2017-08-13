import json
import rethinkdb as r

"""
Script zum Erstellen der Datebank und den Tabellen
"""
CONFIG_FILE = 'config.json'

# config laden
with open(CONFIG_FILE) as fp:
    config = json.load(fp)

DB_HOST = config['db_host']
DB_PORT = config['db_port']

if __name__ == "__main__":
    try:
        print "Initializing database"
        r.db_create('vor').run(r.connect(DB_HOST, DB_PORT))

        r.db('vor').table_create('key_frame_predictions').run(r.connect(DB_HOST, DB_PORT, 'vor'))
        r.db('vor').table_create('key_frames').run(r.connect(DB_HOST, DB_PORT, 'vor'))
        r.db('vor').table_create('videos').run(r.connect(DB_HOST, DB_PORT, 'vor'))

        r.table('key_frame_predictions').index_create('node').run(r.connect(DB_HOST, DB_PORT, 'vor'))
        print "Database initialized"
    except r.ReqlRuntimeError:
        print "Database already initialized"
