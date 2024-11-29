import psycopg2
from numpy.random.mtrand import random
from faker import Faker

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


def generate_int(a, b):
    return random() % (b - a + 1) + a


def main():
    fake.user_name()
    conn = psycopg2.connect(dbname='postgres', user='postgres',
                            password='123', host='localhost')
    cursor = conn.cursor()
    tmp_timestamp = psycopg2.Timestamp(int(random() + 1), int(random() % 11 + 1), int(random() % 20 + 1))
    insert_users(cursor)
    # sql = 'INSERT INTO channel (channel_id, owner_id, name, subscounter, description, regdate) values(?, ?, ?, ?, ?, ?)'
    # cursor.execute("INSERT INTO channel (channel_id, owner_id, name, subscounter, description, regdate) "
    #                "VALUES (generate_series(1, 1000), NULL, 'test_name', generate_series(1, 1000), "
    #                "'default_desc', {})".format(tmp_timestamp))
    print(1)
    cursor.execute("SELECT * FROM \"User\"")
    # data = [
    #     (generate_int(1, 1000), None, generate_name())
    # ]
    # print(data)
    # insert_users(conn)
    for row in cursor:
        print(row)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()