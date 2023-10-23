import sqlite3

# configure the db connnection
connection = sqlite3.connect("budget.db", check_same_thread=False)
# configure a connection cursor
cur = connection.cursor()

def select_recent_expenses(user_id, number):
    cur.execute(
        "SELECT id, amound, type, spent_at FROM transactions WHERE user_id = ? ORDER BY spent_at DESC LIMIT ?",
        [user_id,
        number,]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    
    answer = []
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer


def select_sum_of_category(user_id, number):
    answer = []

    cur.execute(
        "SELECT SUM(amound) as sum, type FROM transactions WHERE user_id = ? GROUP BY type ORDER BY spent_at DESC LIMIT ?",
        [user_id,
        number,]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer


def select_sum_of_category_by_date(user_id, date_str):
    answer = []
    cur.execute(
        "SELECT SUM(amound) AS sum, type FROM transactions WHERE user_id = ? AND spent_at LIKE ? GROUP BY type",
        [user_id,
        date_str + "%",]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer


def select_sum_by_date(user_id, date_str):
    answer = []
    cur.execute(
        "SELECT SUM(amound) AS sum, spent_at FROM transactions WHERE user_id = ? AND spent_at LIKE ? GROUP BY spent_at",
        [user_id,
        date_str + "%",]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer
    

def select_sum_by_month(user_id, date_str):
    answer = []   
    cur.execute(
        "SELECT SUM(amound) AS sum,  STRFTIME('%Y-%m', spent_at) as spent_at FROM transactions WHERE user_id = ? AND spent_at LIKE ? GROUP BY STRFTIME('%Y-%m', spent_at)",
        [user_id,
        date_str + "%",]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer