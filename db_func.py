import sqlite3 as sq


def create_db():
    """Создание базы данных."""
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
    """Уничтожение таблицы в базе данных."""
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS users")


def write_expense(date, name, category, sum):
    """Запись данных о трате в базу."""
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        dat = [date, name, category, sum]

        cur.execute("INSERT INTO users (date, name, category, sum) "
                    "values(?,?,?,?)", dat)


def show_spendings(date, name):
    """Выборка трат за день"""
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        dat = [date, name]

        cur.execute("SELECT sum, category FROM users "
                    "where date == (?) and name == (?)", dat)
        result = cur.fetchall()
        return result


def show_spendings_for_month(date, name):
    """Выборка трат за текущий месяц"""
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        dat = [date, name]

        cur.execute("SELECT sum, category FROM users where "
                    "strftime('%Y-%m', date) == (?) and name == (?) "
                    "GROUP BY category, sum ORDER BY -sum", dat)
        result = cur.fetchall()

        return result


def show_spendings_for_past_month(date, name):
    """Выборка трат за прошлый месяц"""
    with sq.connect('expense.db') as con:
        cur = con.cursor()
        dat = [date, name]
        cur.execute("SELECT sum, category FROM users where "
                    "strftime('%Y-%m', date) == (?) and name == (?) "
                    "GROUP BY sum ORDER BY -sum", dat)
        result = cur.fetchall()
        return result
