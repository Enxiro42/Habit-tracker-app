from db import add_counter, increment_counter


# Creation of main counter Class
class HabitCounter:
    def __init__(self, name: str, description: str, period: str):
        """
        Initializes a new HabitCounter instance to manage and track habit occurrences.

        :param name: The unique name of the habit.
        :param description: A brief description of the habit.
        :param period: The frequency of the habit ('Daily' or 'Weekly').
        """
        self.name = name
        self.description = description
        self.period = period

    def __str__(self):
        """
        Provides a string representation of the HabitCounter instance.

        :return: A formatted string with the name and description of the habit.
        """
        return f"{self.name}: {self.description}"

    def store(self, db):
        """
        Stores the habit data in the database.

        :param db: The database connection object.
        """
        add_counter(db, self.name, self.description, self.period)

    def add_event(self, db, date: str = None):
        """
        Adds a new check-off event for the habit on a specified date.

        :param db: The database connection object.
        :param date: The date of the event. If not provided, defaults to the current date.
        :return: The result of the increment operation, indicating success or failure.
        """
        return increment_counter(db, self.name, date)

