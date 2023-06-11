import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """Drop any existing tables from sparkifydb.
    """
    for query in drop_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Issue dropping table: " + query)
            print(e)

    print("Tables dropped successfully.")

def create_tables(cur, conn):
    """Create new tables (songplays, users, artists, songs, time)
        to sparkify database.
    """
    for query in create_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print("Error: Issue creating table: " + query)
            print(e)
    print("Tables created successfully.")

def main():
    """Connect to AWS Redshift, create new DB (sparkifydb),
        drop any existing tables, create new tables. Close DB connection.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
