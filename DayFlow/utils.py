from datetime import datetime


def display_task_list(tasks):
    """Print a list of tasks, or a friendly message if none exist."""
    if not tasks:
        print("No tasks to display.")
        return

    for task in tasks:
        print(task.display())


def prompt_for_priority():
    """Prompt the user for a valid priority number."""
    while True:
        try:
            priority = int(input("Enter priority (1=Highest, 2=High, 3=Medium, 4=Low, 5=Lowest): "))
            if 1 <= priority <= 5:
                return priority
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid integer.")


def prompt_for_due_date():
    """Prompt the user for a due date that is not in the past."""
    while True:
        due_date_str = input("Enter due date and time (YYYY-MM-DD HH:MM): ")
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date format. Please try again.")
            continue

        if due_date < datetime.now():
            print("Due date cannot be in the past.")
            continue

        return due_date
