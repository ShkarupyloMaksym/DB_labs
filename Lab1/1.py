import threading
import time
import psycopg2

username = 'Shkarupylo'
password = 'Shkarupylo'
database = 'labs'
host = 'localhost'
port = '5432'


def lost_update():
    conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
    cursor = conn.cursor()

    for i in range(10000):
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
        counter = cursor.fetchone()[0]

        counter += 1
        cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = %s", (counter, 1))
        conn.commit()

    conn.close()


def in_place_update():
    conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
    cursor = conn.cursor()
    for i in range(10000):
        cursor.execute("update user_counter set counter = counter + 1 where user_id = %s", (1,))
        conn.commit()

    conn.close()


def row_level_locking():
    conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
    cursor = conn.cursor()

    for i in range(10000):
        cursor.execute(("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE"))
        counter = cursor.fetchone()[0]
        counter = counter + 1

        cursor.execute("update user_counter set counter = %s where user_id = %s", (counter, 1))
        conn.commit()

    conn.close()


def optimistic_concurrency_control():
    conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
    cursor = conn.cursor()

    for i in range(10000):
        while True:
            cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
            counter, version = cursor.fetchone()
            counter = counter + 1

            cursor.execute("update user_counter set counter = %s, version = %s where user_id = %s and version = %s",
                           (counter, version + 1, 1, version))
            conn.commit()
            count = cursor.rowcount

            if count > 0:
                break

    conn.close()


start_time = time.time()

threads = []
for i in range(10):
    thread = threading.Thread(target=lost_update)
    # thread = threading.Thread(target=in_place_update)
    # thread = threading.Thread(target=row_level_locking)
    # thread = threading.Thread(target=optimistic_concurrency_control)

    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(round(time.time() - start_time, 3), "seconds")
