# My Tracking App

Welcome to My Tracking App! This application is designed to help users manage and track various habits over time, analyzing their consistency and progress through simple and interactive tools. This project is part of my Object-Oriented Programming (OOP) Python course at the university and serves as a portfolio project to demonstrate my learning and application of software development principles.

## What is it?

My Tracking App is a habit tracking system that allows users to set up daily or weekly habits, track their completions, and view their progress over time. This app helps the users stay on track and visualize your consistency and streaks.

## Installation

To get started with My Tracking App, you need to install at least Python 3.7 and the required Python packages. After that just run the following command in your terminal:

```shell
pip install -r requirements.txt
```

## Usage

To use My Tracking App, start the application by running the following command in your project directory:

```shell
python main.py
```
Please follow the on-screen instructions to manage and track your habits.

## Tests
To run the tests for the application, use pytest. Execute the following command in your project directory:

```shell
pytest .
```
## Database Configuration
You can switch between test and production environments by changing the database name in db.py. In line 6, change the database file name from test.db to main.db or vice versa:

- Use main.db for normal operations.
- Use test.db for testing and development purposes.

## Features

My Tracking App offers a variety of features to enhance your habit tracking experience:

- **Habit Setup**: Easily set up and customize habits with daily or weekly frequencies.
- **Habit Tracking**: Log each time you complete a habit, automatically updating your progress.
- **Progress Visualization**: View visual representations of your habit streaks and consistency over time.
- **Streak Analysis**: Analyze the longest streaks you've achieved and view detailed records of your past performances.
- **Interactive CLI**: Utilize a user-friendly command-line interface to interact with the app, making it easy to manage your habits.

These features are designed to provide a comprehensive and intuitive user experience, helping you stay motivated and consistent with your habits.


