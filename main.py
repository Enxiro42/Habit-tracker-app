import questionary
from analyse import print_all_counter_data, streak_analysis
from db import get_db, get_all_counter_names, delete_habit, get_last_check
from class_counter import HabitCounter


def counter_choice(db, include_all_option=False):
    """
    Presents a list of habit names to the user for selection, optionally including an "All" option.

    :param db: an initialized sqlite3 database connection
    :param include_all_option: boolean indicating whether to include the "Overall" option in the selection list
    :return: the name of the selected habit, None for going back or Overall if needed
    """

    counter_names = get_all_counter_names(db)
    if include_all_option:
        counter_names.append("Overall")  # Append the "All" option if requested
    counter_names.append("Go Back")  # Append the "Go Back" option

    name = questionary.select(
        "Please select a habit",
        choices=counter_names
    ).ask()
    if name == "Go Back":
        print("Action cancelled.")
        return None  # Explicitly return None to indicate cancellation
    else:
        return name  # Return the selected habit name or "All"


def cli():
    db = get_db()
    questionary.confirm("Are you ready to rumble?").ask()

    stop = False
    while not stop:
        choice = questionary.select(
            "What would you like to do?",
            choices=["Create a new habit", "Delete a habit", "Check off habit", "See last check offs",
                     "Analyse habits", "Quit program"]
        ).ask()

        if choice == "Create a new habit":
            counter_names = get_all_counter_names(db)
            name = questionary.text("What shall be the name of your habit?").ask()
            while name in counter_names:
                name = questionary.text("The provided habit name already exists. Please enter another one:").ask()
            desc = questionary.text("What is the description of your habit").ask()
            period = questionary.select(
                "Please select the period of your habit",
                choices=["Daily", "Weekly"]
            ).ask()
            counter = HabitCounter(name, desc, period)
            counter.store(db)  # uses the store method from habitcounter class
            print("Habit was set up successfully")

        elif choice == "Delete a habit":
            name = counter_choice(db)  # Invoke the function to get user's choice
            if name is None:  # If the user chose "Go Back", cancel the action
                continue  # Return early to go back to the main menu
                # Proceed with the action for the selected habit
            confirmation = questionary.select(f"Are you sure that you want to delete the habit {name}?",
                                              choices=["Yes", "No"]).ask()
            if confirmation == "Yes":
                delete_habit(db, name)
            else:
                continue

        elif choice == "Check off habit":
            name = counter_choice(db)
            if name is None:
                continue
            counter = HabitCounter(name, "", "")
            check_off_allowed = counter.add_event(db)
            print(f"Check-off allowed: {check_off_allowed}")  # Debugging output

        elif choice == "See last check offs":
            name = counter_choice(db)
            if name is None:
                continue
            checklist = get_last_check(db, name)
            print(checklist)

        elif choice == "Analyse habits":
            choice = questionary.select(
                "Please select",
                choices=["See all habits", "See daily habits", "See weekly habits", "See streaks", "Go back"]
            ).ask()
            if choice == "See all habits":
                print_all_counter_data(db, "Daily")
                print_all_counter_data(db, "Weekly")
            elif choice == "See daily habits":
                print_all_counter_data(db, "Daily")
            elif choice == "See weekly habits":
                print_all_counter_data(db, "Weekly")
            elif choice == "See streaks":
                name = counter_choice(db, include_all_option=True)
                if name is None:
                    continue
                else:
                    streak_analysis(db, name)
            else:
                continue

        else:
            print("Goodbye and have a great day!")
            stop = True


if __name__ == "__main__":
    cli()
