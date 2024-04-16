import matplotlib.pyplot as plt
from datetime import date, timedelta
from db import get_streak_data, get_all_counter_data, get_habit_info


def streak_analysis(db, name):
    """
    Analyzes streak data for a specific habit or all habits, presenting the longest streak
    and optionally visualizing streak history with a bar chart.

    :param db: An initialized sqlite3 database connection.
    :param name: The name of the habit to analyze, or "Overall" for analyzing all habits.
    :return: None. Outputs analysis results to console and optionally displays a bar chart.
    """
    streak_data = get_streak_data(db, name)

    # Check if there is any streak data available
    if not streak_data:
        print("No streak data found.")
        return  # Early return if no data is found

    # Extracting all dates and streak lengths into lists
    all_dates = [streak[0] for streak in streak_data]
    all_lengths = [streak[2] for streak in streak_data]

    # Finding the longest streak and its index
    max_length = max(all_lengths)
    index = all_lengths.index(max_length)

    if name == "Overall":
        # Extracting all habit names for "Overall" analysis
        all_habits = [streak[1] for streak in streak_data]
        print(f"The longest streak you have achieved was {all_lengths[index]} times in a row in "
              f"{all_habits[index]} on {all_dates[index]}.")
    else:
        # Visualizing streak history for a specific habit with a bar chart
        plt.bar(all_dates, all_lengths)
        plt.title(name)
        plt.xlabel('Achievement Dates')
        plt.ylabel('Achieved Streaks')
        plt.xticks(rotation=45)

        print(f"The longest streak you have achieved in {name} was {all_lengths[index]} times in a row "
              f"on {all_dates[index]}."
              f"\n\nYour streak history is as follows:\n")
        plt.show()


def print_all_counter_data(db, period):
    """
    Prints all habit entries from the 'counter' table in the database for a specific period.

    :param db: The database connection object, used for querying the database.
    :param period: The period of the habits to filter by (e.g., 'Daily', 'Weekly'), which determines which habits are
     displayed.
    """

    all_counters = get_all_counter_data(db, period)  # Use the function to retrieve data
    # Check if there are any entries
    if all_counters:
        for counter in all_counters:
            print(f"Name: {counter[0]}, Description: {counter[1]}, Period: {counter[2]}, Current Count: {counter[3]}\n")
    else:
        print(f"No {period} habits found.")


def reset_decision(db, name, event_date_str):
    """
    Determines whether a reset is necessary based on the last check-off date and the period of the habit.

    :param db: The database connection object.
    :param name: Name of the habit present in the database.
    :param event_date_str: Optional. The date string for the current reset attempt, in the format "YYYY-MM-DD".
                           Defaults to today's date if not provided.
    :return: A boolean value. Returns True if a reset is necessary, otherwise False.
    """
    last_date_str, period = get_habit_info(db, name)

    if last_date_str is None:
        print("reset decision is None")
        return False  # No previous date means no need for a reset

    last_date = date.fromisoformat(last_date_str)
    event_date = date.fromisoformat(event_date_str)  # Ensure event_date_str is a date object for comparison
    allowed_difference = timedelta(days=1 if period == 'Daily' else 7)

    # Return True if the time difference is greater than the allowed difference
    difference = event_date - last_date
    print(f"Event Date: {event_date}")
    if difference > allowed_difference:
        print(f"reset decision is true, difference: {difference}")
        return True
    else:
        print(f"reset decision is false, difference: {difference}")
        return False


def checkoff_decision(db, name, event_date_str=None):
    """
    Determines whether a check-off is allowed based on the last check-off date and the period of the habit.

    :param db: The database connection object.
    :param name: Name of the habit present in the database.
    :param event_date_str: Optional. The date string for the current check-off attempt, in the format "YYYY-MM-DD".
                           Defaults to today's date if not provided.
    :return: A boolean value. Returns True if a check-off is allowed, otherwise False.
    """
    last_date_str, period = get_habit_info(db, name)
    if not event_date_str:
        event_date_str = str(date.today())  # Default to today's date if not provided

    if last_date_str is None:
        print("checkoff decision is True (no previous date)")
        return True  # If no previous check-off date, allow check-off

    last_date = date.fromisoformat(last_date_str)
    event_date = date.fromisoformat(event_date_str)  # Ensure event_date_str is a date object for comparison
    allowed_difference = timedelta(days=1 if period == 'Daily' else 7)

    # Check if the time difference is at least the allowed difference
    difference = event_date - last_date
    print(f"Event Date: {event_date}")
    if difference >= allowed_difference:
        print(f"checkoff decision is true, difference: {difference}")
        return True
    else:
        print(f"checkoff decision is false, difference: {difference}")
        return False
