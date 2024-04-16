# import os
from datetime import datetime, timedelta
import random
from class_counter import HabitCounter
from db import get_db


class TestCounter:
    def setup_method(self):
        # Creating a test database
        self.db = get_db("test.db")
        self.counters = []

        # Define daily and weekly counters
        daily_habits = [("Drink Water", "Drink at least 8 glasses of water", "Daily"),
                        ("Read", "Read for at least 30 minutes", "Daily"),
                        ("Exercise", "Do some form of exercise", "Daily")]
        weekly_habits = [("Clean House", "Weekly house cleaning", "Weekly"),
                         ("Call Family", "Call family members", "Weekly")]

        # Adding counters to the database using the store method of HabitCounter
        for habit in daily_habits + weekly_habits:
            name, description, period = habit
            counter = HabitCounter(name, description, period)
            counter.store(self.db)  # saves counter into db
            self.counters.append(counter)  # HabitCounter instance added to list

        # Generate random check - offs for the first 29 days for each habit
        start_date = datetime.strptime("2024-03-10", "%Y-%m-%d")  # Start from March 10th
        for day in range(25):  # Generate entries for the first 29 days
            current_date = start_date + timedelta(days=day)
            for counter in self.counters:
                # Randomly skip some days for daily and weekly habits
                if random.choice([True, False]):
                    event_date_str = current_date.strftime("%Y-%m-%d")
                    counter.add_event(self.db, event_date_str)

        today = datetime.now()
        for counter in self.counters:
            for days_back in [12, 11, 9, 8, 7, 6, 5, 3, 2, 1]:
                date_str = (today - timedelta(days=days_back)).strftime("%Y-%m-%d")
                counter.add_event(self.db, date_str)

    def test_counter_logic1(self):
        #  for days_back in [2, 3]:  # For the last two days
        #
        pass

    def teardown_method(self):
        self.db.close()
        #  if os.path.exists("test.db"):
        #    os.remove("test.db")
