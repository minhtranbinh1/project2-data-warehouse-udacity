import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Load JSON input data (log_data and song_data) from S3 and insert
        into staging_events and staging_songs tables.
    """
    print("Start loading data from S3 to AWS Reshift tables...")

    for query in copy_table_queries:
        print('------------------')
        print('Processing query: {}'.format(query))
        cur.execute(query)
        conn.commit()
        print('------------------')
        print('{} processed OK.'.format(query))

    print('All files COPIED OK.')



def insert_tables(cur, conn):
    """Insert data from staging tables (staging_events and staging_songs)
        into star schema analytics tables:
        * Fact table: songplays
        * Dimension tables: users, songs, artists, time
    """
    print("Start inserting data from staging tables into analysis tables...")
    for query in insert_table_queries:
        print('------------------')
        print('Processing query: {}'.format(query))
        cur.execute(query)
        conn.commit()
        print('{} processed OK.'.format(query))

    print('All files INSERTED OK.')

def main():
    """Connect to DB and call
        * load_staging_tables to load data from JSON files
            (song_data and log_data in S3) to staging tables and
        * insert_tables to insert data to analysis tables.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"
                            .format(*config['CLUSTER']
                            .values()))
    cur = conn.cursor()
    print("AWS Redshift connection established OK.")

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
