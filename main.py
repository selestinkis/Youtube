import psycopg2
from numpy.random.mtrand import random
from faker import Faker
import random
from scripts.regsetup import description

fake = Faker(['en_US', 'ru_RU'])


def insert_users(cur, count=1000):
    # Используем множества для отслеживания уникальных значений
    unique_logins = set()
    unique_emails = set()

    for _ in range(count):
        while True:
            login = fake.user_name()
            email = fake.email()
            if login not in unique_logins and email not in unique_emails:
                unique_logins.add(login)
                unique_emails.add(email)
                break  # Уникальные значения найдены, можно выйти из цикла

        username = fake.user_name()
        password = fake.password()
        name = fake.first_name()
        surname = fake.last_name()
        patronymic = fake.middle_name()
        registration_date = fake.date_time_this_year()

        cur.execute("INSERT INTO \"User\" (regDate, surname, \"name\", patronymic, nick, email, pass) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", (registration_date, surname, name, patronymic, username, email, password))
        # cur.execute("SELECT * FROM \"User\"")
        # for row in cur:
        #     print(row)


def insert_channel (cur):
    cur.execute("SELECT user_id FROM \"User\"")
    users = [uid[0] for uid in cur.fetchall()]

    cur.execute("SELECT \"name\" FROM Channel")
    existing_names = set(nid[0] for nid in cur.fetchall())

    description = ""

    for user in users:
        while True:
            name = fake.user_name()
            if name not in existing_names:
                existing_names.add(name)
                break
        description = fake.text(max_nb_chars=1000)


        cur.execute("INSERT INTO Channel (owner_id, name, subscounter, description, regdate) "
                    "VALUES (%s, %s, %s, %s, %s)", (user, name, random.randint(1, 100000), description, fake.date()))

def insert_video(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    name = fake.text(max_nb_chars=100)
    description = fake.text(max_nb_chars=1000)
    channel = random.choice(channels)
    type = random.randint(0, 1) == 1
    cur.execute("INSERT INTO Video (publisher_id, name, publicationdate, timecodes, description, likescount, dislikescount, type, length) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (channel, name, fake.date_time(), fake.time(), description, random.randint(0, 1000000), random.randint(0, 1000000), type, fake.time()))

def insert_post(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    text = fake.text(max_nb_chars=1000)
    channel = random.choice(channels)
    cur.execute("INSERT INTO Post (channel_id, text)  "
                "VALUES (%s, %s)", (channel, text))


def insert_comment(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    cur.execute("SELECT comment_id FROM \"Comment\"")
    comments = [cid[0] for cid in cur.fetchall()]
    cur.execute("SELECT video_id FROM Video")
    videos = [cid[0] for cid in cur.fetchall()]
    cur.execute("SELECT post_id FROM Post")
    posts = [cid[0] for cid in cur.fetchall()]
    text = fake.text(max_nb_chars=1000)
    channel = random.choice(channels)
    comment = None
    coin = random.randint(0, 1)
    if len(comments) != 0 and coin == 1:
        comment = random.choice(comments)
    coin = random.randint(0, 1)
    if coin == 0:
        video = random.choice(videos)
        post = None
    elif coin == 1:
        post = random.choice(posts)
        video = None
    cur.execute("INSERT INTO \"Comment\" (parent_id, channel_id, related_video_id, related_post_id, content, likescount, dislikescount, publicationdate)  "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (comment, channel, video, post, text, random.randint(0, 1000000), random.randint(0, 1000000), fake.date()))


def insert_playlist(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    cur.execute("SELECT video_id FROM Video")
    videos = [cid[0] for cid in cur.fetchall()]
    channel = random.choice(channels)
    video = random.choice(videos)
    name = fake.text(max_nb_chars=100)
    cur.execute("INSERT INTO Playlist (channel_id, video_id, name, lastchangedate, viewscount) "
                "VALUES (%s, %s, %s, %s, %s)", (channel, video, name, fake.date_time(), random.randint(0, 1000000)))


def insert_complaint(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    cur.execute("SELECT video_id FROM Video")
    videos = [cid[0] for cid in cur.fetchall()]
    channel = random.choice(channels)
    video = random.choice(videos)
    cur.execute("INSERT INTO Complaint (channel_id, video_id) "
                "VALUES (%s, %s)", (channel, video))


def insert_live(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    channel = random.choice(channels)
    cur.execute("INSERT INTO livetranslation (channel_id, audienscount, starttime) "
                "VALUES (%s, %s, %s)", (channel, random.randint(0, 10000), fake.date_time()))


def insert_chat(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    channel = random.choice(channels)
    cur.execute("SELECT translation_id FROM Livetranslation")
    lives = [cid[0] for cid in cur.fetchall()]
    live = random.choice(lives)
    cur.execute("INSERT INTO Chat (translation_id, chanel_id, messagetext) "
                "VALUES (%s, %s, %s)", (live, channel, fake.text(max_nb_chars=100)))


def insert_rate(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    channel = random.choice(channels)
    cur.execute("SELECT video_id FROM video")
    videos = [cid[0] for cid in cur.fetchall()]
    video = random.choice(videos)
    cur.execute("INSERT INTO rate (video_id, channel_id, rate) "
                "VALUES (%s, %s, %s)", (video, channel, random.randint(0, 2)))


def insert_subscription(cur):
    cur.execute("SELECT channel_id FROM Channel")
    channels = [cid[0] for cid in cur.fetchall()]
    channel = random.choice(channels)
    while True:
        channel2 = random.choice(channels)
        if channel2 != channel:
            break
    cur.execute("INSERT INTO \"Subscription\" (subscriptor_id, channel_id) "
                "VALUES (%s, %s)", (channel, channel2))


def insert_tag(cur):
    cur.execute(f"INSERT INTO tag (name) VALUES (\'{fake.text(max_nb_chars=100)}\')")


def insert_tag_video(cur):
    cur.execute("SELECT video_id FROM video")
    videos = [cid[0] for cid in cur.fetchall()]
    video = random.choice(videos)
    cur.execute("SELECT tag_id FROM tag")
    tags = [cid[0] for cid in cur.fetchall()]
    tag = random.choice(tags)
    cur.execute("INSERT INTO tag_video (video_id, tags_id) "
                "VALUES (%s, %s)", (video, tag))


def insert_playlist_video(cur):
    cur.execute("SELECT playlist_id FROM playlist")
    playlists = [cid[0] for cid in cur.fetchall()]
    playlist = random.choice(playlists)
    cur.execute("SELECT video_id FROM video")
    videos = [cid[0] for cid in cur.fetchall()]
    video = random.choice(videos)
    cur.execute("INSERT INTO playlist_video (playlist_id, video_id) VALUES (%s, %s)", (playlist, video))



def main():
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='123', host='localhost')
    cursor = conn.cursor()
    n = 100000
    insert_users(cursor, n)
    for i in range(0, n):
        insert_channel(cursor)
        insert_video(cursor)
        insert_post(cursor)
        insert_comment(cursor)
        insert_complaint(cursor)
        insert_live(cursor)
        insert_playlist(cursor)
        insert_playlist_video(cursor)
        insert_rate(cursor)
        insert_subscription(cursor)
        insert_tag(cursor)
        insert_tag_video(cursor)
        insert_chat(cursor)
    conn.commit()
    conn.close()
    fake.

if __name__ == '__main__':
    # print(random.randint(0, 1))
    main()