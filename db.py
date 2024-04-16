import sqlite3
from datetime import date


# database creation as a function
def get_db(name="test.db"):  # test.db is temporary, main.db is for normal use
    db = sqlite3.connect(name)
    # internal creation of tables
    create_table(db)
    return db


# defining of tables after creating the database
def create_table(db):  # db parameter (return value of function get_db) is connected against the database
    # cursor is created from the database
    # the cursor can be used to execute sql commands for us
    with db:
        cur = db.cursor()    # creation of counter table via cursor
        cur.execute("""CREATE TABLE IF NOT EXISTS counter (
            name TEXT PRIMARY KEY,
            description TEXT,
            period TEXT,
            current_count INT DEFAULT 0)""")  # Default value set to 0

        # creation of tracker table for storing the increments
        # tracker is connected to counter via foreign key (counterName) to the counter table
        cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
            date TEXT,
            counterName TEXT, 
            FOREIGN KEY(counterName) REFERENCES counter(name))""")

        cur.execute("""CREATE TABLE IF NOT EXISTS streaks (
                    date TEXT,
                    counterName TEXT,
                    length INT,
                    FOREIGN KEY(counterName) REFERENCES counter(name))""")

    db.commit()
    # This method sends a COMMIT statement to the MySQL server, committing the current transaction. Since by default
    # Connector/Python does not autocommit, it is important to call this method after every transaction that modifies
    # data for tables that use transactional storage engines.


# the next 3 functions are for database storage/manipulation
def add_counter(db, name, description, period):
    with db:
        cur = db.cursor()
        cur.execute("INSERT INTO counter (name, description, period) VALUES (?, ?, ?)", (name, description, period))
    db.commit()


def add_streak(db, name, event_date):
    """
    Adds a new streak entry to the streaks table in the database and resets the current count.

    :param db: An initialized SQLite3 database connection.
    :param name: The name of the habit associated with the streak.
    :param event_date: The date when the streak was achieved. Defaults to today's date if not provided.
    """
    # Defaulting event_date to today's date if it's not provided
    if not event_date:
        event_date = str(date.today())

    with db:
        cur = db.cursor()
        cur.execute("SELECT current_count FROM counter WHERE name = ?", (name,))
        length = cur.fetchone()[0]

        # Inserting the new streak entry into the database
        cur.execute("INSERT INTO streaks (date, counterName, length) VALUES (?, ?, ?)", (event_date, name, length))

        # Resetting the current count in the counter table
        cur.execute("UPDATE counter SET current_count = 1 WHERE name = ?", (name,))
        db.commit()
        print(f"Streak for '{name}' has been recorded and counter has been resetted to 1.")


def increment_counter(db, name, event_date=None):
    """
    Inserts a check-off event for a habit into the tracker table and updates the habit's count in the database.
    It checks if the habit is allowed to be checked off based on its period and the last check-off date.
    If a reset is necessary (determined by the reset_decision function), a new streak is added and the count is reset.
    Otherwise, the current count is incremented.

    :param db: An initialized SQLite3 database connection. It provides the methods to interact with the database.
    :param name: The name of the habit to check off. This is used to identify the habit in the database.
    :param event_date: Optional. The date of the event. Defaults to today's date if not provided. This is used to
                       record when the habit was checked off.
    :return: True if the check-off event was successfully added and False if not allowed.
             It also commits the transaction to the database after modifying the data.
    """
    from analyse import checkoff_decision, reset_decision

    if not event_date:
        event_date = str(date.today())

    if not checkoff_decision(db, name, event_date):
        print(f"The habit '{name}' cannot be checked off today ({event_date}).")
        return False

    with db:
        cur = db.cursor()
        if reset_decision(db, name, event_date):
            add_streak(db, name, event_date)
        else:
            cur.execute("UPDATE counter SET current_count = current_count + 1 WHERE name = ?", (name,))
        cur.execute("INSERT INTO tracker (date, counterName) VALUES (?, ?)", (event_date, name))
        print(f"Habit '{name}' successfully checked off for today ({event_date}).")

        db.commit()

    return True


def get_last_check(db, name):
    """
    Retrieves all check-off events for a specific habit from the 'tracker' table.

    :param db: The database connection object. This is used to execute SQL commands.
    :param name: The name of the habit whose check-off events are to be retrieved.
    :return: A list of tuples where each tuple represents a check-off event associated with the habit.
    """
    with db:
        cur = db.cursor()
        cur.execute("SELECT * FROM tracker WHERE counterName = ?", (name,))
        checklist = cur.fetchall()
        return checklist


def get_habit_info(db, name):
    """
    Retrieves the last check-off date and the period of a specific habit.

    :param db: The database connection object.
    :param name: The name of the habit.
    :return: A tuple containing the last check-off date (as a string) and the period.
    """
    with db:
        cur = db.cursor()
        cur.execute("SELECT MAX(date) FROM tracker WHERE counterName = ?", (name,))
        last_date = cur.fetchone()[0]

        cur.execute("SELECT period FROM counter WHERE name = ?", (name,))
        result = cur.fetchone()
        period = result[0] if result else None

        if last_date is None or period is None:
            print(f"get_habit_info last date none")  # Debug Output
            return None, None

    print(f"get_habit_info last date exists")  # debug output
    print(f"Last Check-off Date: {last_date}")
    return last_date, period


def get_all_counter_data(db, period):
    """
    Retrieves all habit entries from the 'counter' table in the database that match the specified period.

    Parameters:
    - db: The database connection object.
    - period: The period of the habits to retrieve.

    Returns:
    - A list of tuples, each representing a habit entry that matches the specified period.
    """
    with db:
        cur = db.cursor()
        # Using parameterized SQL query to prevent SQL injection
        cur.execute("SELECT * FROM counter WHERE period = ?", (period,))
        counter_list = cur.fetchall()
        return counter_list


def get_streak_data(db, name):
    """
    Retrieves streak data for a specific habit or all habits from the 'streaks' table.

    :param db: an initialized sqlite3 database connection.
    :param name: the name of the habit to retrieve streak data for, or "Overall" to retrieve data for all habits.
    :return: a list of tuples containing the streak data.
    """
    with db:
        cur = db.cursor()
        if name == "Overall":
            cur.execute("SELECT * FROM streaks")
        else:
            cur.execute("SELECT * FROM streaks WHERE counterName=?", (name,))
        return cur.fetchall()


def get_all_counter_names(db):
    """
    Retrieves a list of habit names from the 'counter' table in the database.

    :param db: The database connection object used to execute SQL commands.
    :return: A list of strings where each string represents a unique habit name stored in the database.
    """
    with db:
        cur = db.cursor()
        cur.execute("SELECT name FROM counter")  # Execute SQL query to select habit names
        all_counters = cur.fetchall()  # Fetch all results of the query
        return [counter[0] for counter in all_counters]  # Return names extracted from tuples


def delete_habit(db, name):
    """
    Deletes a habit and its related entries from both the counter and tracker tables based on its name.

    Parameters:
    - db: The database connection object.
    - name: The name of the habit to delete.
    """
    with db:
        cur = db.cursor()
        # First, delete related entries from the tracker table
        cur.execute("DELETE FROM tracker WHERE counterName = ?", (name,))
        # Then, delete the habit from the counter table
        cur.execute("DELETE FROM counter WHERE name = ?", (name,))
        # Commit the changes to the database
        db.commit()
        print(f"Habit '{name}' and its related entries were deleted successfully.")
