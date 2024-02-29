import threading
import time
import psycopg2

db_params = {
    "host": "db",
    "database": "postgres",
    "user": "postgres",
    "password": "docker",
    "port": "5432",
}
num_of_instances = range(1, 10_000 + 1)

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {args[0].__name__} took {round(end - start)} seconds")
        return result

    return wrapper


def db_function(method):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        method(conn, cursor)
        cursor.close()
        conn.close()

    return wrapper


@db_function
def make_counter_one(conn, cursor):
    cursor.execute("update user_counter set counter = 0 where user_id = 1")
    cursor.execute("update user_counter set version = 0 where user_id = 1")
    conn.commit()


@db_function
def check_counter(conn, cursor):
    cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
    final_counter = cursor.fetchone()[0]
    print(f"Counter is {final_counter}")


@db_function
def lost_update(conn, cursor):
    for _ in num_of_instances:
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
        counter = cursor.fetchone()[0]
        counter = counter + 1
        cursor.execute("update user_counter set counter = {} where user_id = {}".format(counter, 1))
        conn.commit()


@db_function
def inplace_update(conn, cursor):
    for _ in num_of_instances:
        cursor.execute("update user_counter set counter = counter + 1 where user_id = {}".format(1))
        conn.commit()


@db_function
def row_level_locking(conn, cursor):
    for _ in num_of_instances:
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
        counter = cursor.fetchone()[0]
        counter = counter + 1
        cursor.execute("update user_counter set counter = {} where user_id = {}".format(counter, 1))
        conn.commit()


@db_function
def optimistic_concurrency_control(conn, cursor):
    for _ in num_of_instances:
        while True:
            cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
            (counter, version) = cursor.fetchone()
            counter = counter + 1
            cursor.execute("update user_counter set counter = {}, version = {} "
                           "where user_id = {} and version = {}".format(counter, version + 1, 1, version))
            conn.commit()
            count = cursor.rowcount
            if count > 0:
                break


@timer_decorator
def task_by_func(task):
    thread_num = 10

    thread_pool = [threading.Thread(target=task) for _ in range(thread_num)]

    for thread in thread_pool:
        thread.start()

    for thread in thread_pool:
        thread.join()

    print("tasks have finished")


if __name__ == "__main__":
    tasks = [lost_update, inplace_update, row_level_locking, optimistic_concurrency_control]
    for k, i in enumerate(tasks):
        print(f'Task {k}:')
        make_counter_one()

        task_by_func(i)

        check_counter()
        print('__________')