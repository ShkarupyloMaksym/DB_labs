import pandas as pd
import psycopg2

from db.get_creds import get_creds
from tabulate import tabulate


def smart_input(inf_text, inp_text, incorrect='Maybe you have mistyped, try again.', can_be_text=lambda x: True):
    print(inf_text)
    while True:
        inp = input(inp_text)
        if can_be_text(inp):
            return inp
        print(incorrect)


def search_data(cursor):
    cursor.execute('SELECT DISTINCT(country) FROM weather_db;')
    countries = [row[0] for row in cursor]

    cursor.execute('SELECT DISTINCT(DATE(last_updated)) FROM weather_db;')
    dates = [str(row[0]) for row in cursor]

    print("You can input country, date and type_table. \n"
          "If you don't want to write something, you can skip by writing '-'")
    country = smart_input('Select country', 'Input country: ',
                          'We haven`t such country', lambda x: x in countries + ['-'])
    date = smart_input('Select date', 'Input date in format yyyy-mm-dd: ',
                       'We haven`t such date', lambda x: x in dates + ['-'])
    type_table = smart_input('Select what do you want to see', 'Weather table, or precipitation? (W/P): ',
                             can_be_text=lambda x: x in list('WP') + ['-'])
    return country, date, type_table


def get_params(country, date):
    if country != '-' and date != '-':
        return 'WHERE country=%s AND last_updated=%s', (country, date)
    elif country != '-':
        return 'WHERE country=%s', (country,)
    elif date != '-':
        return 'WHERE DATE(last_updated)=%s', (date,)
    return '', ()


def data_from_table(cursor):
    country, date, type_table = search_data(cursor)
    cond, params = get_params(country, date)

    if type_table == 'W':
        cursor.execute("""
            SELECT wind_degree, wind_kph, wind_direction, last_updated, sunrise
            FROM weather_db """ + cond + ' ORDER BY last_updated; ', params)

        rows = [row for row in cursor.fetchall()]
        cols = [column[0] for column in cursor.description]

    else:
        cursor.execute("""
            SELECT id, last_updated
            FROM weather_db """ + cond + ' ORDER BY last_updated; ', params)

        all_data = cursor.fetchall()
        idxs = [int(row[0]) for row in all_data]

        cursor.execute(f"""
                SELECT *
                FROM precipitation
                WHERE precipitation_id IN ({','.join(['%s'] * len(idxs))})
            """, idxs)

        rows = [row[2:] for row in cursor.fetchall()]
        cols = [column[0] for column in cursor.description][2:]
    df = pd.DataFrame(rows, columns=cols)

    return df


if __name__ == '__main__':
    conn_data = get_creds()

    conn = psycopg2.connect(**conn_data)
    with conn:
        cursor = conn.cursor()
        df = data_from_table(cursor)
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
