import sqlite3 as sq


def create_db():
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date TEXT,
            name TEXT,
            category TEXT,
            sum INTEGER        
        )""")


def destroy_db():
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS users")


def write_expense(date, name, category, sum):
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        dat = [date, name, category, sum]

        cur.execute("INSERT INTO users (date, name, category, sum) "
                    "values(?,?,?,?)", dat)


def show_today_expensive(date, name):
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        dat = [date, name]

        cur.execute("SELECT * FROM users "
                    "where date == (?) and name == (?)", dat)
        result = cur.fetchall()
        return result
