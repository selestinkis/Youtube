import psycopg2

def selectVideo(cur):
    cur.execute("""
        SELECT * FROM video
    """)

    for row in cur:
        print(row)


def selectVideoDate(cur):
    cur.execute("""
        SELECT * FROM video WHERE publicationdate >= '2000-01-01'
    """)

    for row in cur:
        print(row)


def selectUsersByPlaylist(cur):
    cur.execute("""
        SELECT * FROM "User" WHERE user_id == (SELECT owner_id FROM channel WHERE channel_id == (select channel_id FROM playlist))
    """)

    for row in cur:
        print(row)

def selectUserByChannelsNumber(cur, num):
    cur.execute("""
        SELECT "User".user_id, COUNT(owner_id) AS owner_count FROM "User"
        JOIN channel ON "User".user_id = channel.owner_id
        GROUP BY "User".user_id
        HAVING COUNT(owner_id) > %s
    """, (num -1))

def main():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='123', host='localhost')
    cursor = conn.cursor()

    print("\tAll videos:\n")
    selectVideo(cursor)
    print("\tVideo elder than 1999:\n")
    selectVideoDate(cursor)
    print("\tAll users that have channels with playlists:\n")
    selectUsersByPlaylist(cursor)
    print("\tAll users that have n or more channels:\n")
    selectUserByChannelsNumber(cursor)

if __name__ == '__main__':
    main()