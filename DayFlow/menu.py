from datetime import datetime

from scheduler import UPCOMING_DAYS
from utils import display_task_list, prompt_for_due_date, prompt_for_priority


def add_task_menu(scheduler):
    """Collect task details and add a new task to the scheduler."""
    name = input("Enter task name: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return

    priority = prompt_for_priority()
    due_date = prompt_for_due_date()

    if scheduler.add_task(name, priority, due_date):
        print("Task added successfully!")
    else:
        print("A task with that name already exists.")


def remove_task_menu(scheduler):
    """Remove a task from the scheduler by name."""
    name = input("Enter task name to remove: ")
    if scheduler.remove_task(name):
        print(f"Task '{name}' removed successfully!")
    else:
        print(f"No task named '{name}' found.")


def edit_task_menu(scheduler):
    """Ask which field to edit and update the matching task."""
    name = input("Enter task name to edit: ")
    print("What would you like to edit?")
    print("1. Name")
    print("2. Priority")
    print("3. Due Date")
    field_choice = input("Enter your choice: ")

    if field_choice == "1":
        new_name = input("Enter new name: ").strip()
        if scheduler.edit_task(name, "name", new_name):
            print("Task updated successfully!")
        else:
            print("Unable to update task.")
    elif field_choice == "2":
        new_priority = prompt_for_priority()
        if scheduler.edit_task(name, "priority", new_priority):
            print("Task updated successfully!")
        else:
            print("Unable to update task.")
    elif field_choice == "3":
        new_due_date = prompt_for_due_date()
        if scheduler.edit_task(name, "due_date", new_due_date):
            print("Task updated successfully!")
        else:
            print("Unable to update task.")
    else:
        print("Invalid choice.")


def view_tasks_menu(scheduler):
    """Show a grouped view of the available task lists."""
    print("View Tasks")
    print("1. All Tasks")
    print("2. Completed Tasks")
    print("3. Pending Tasks")
    print("4. Highest Priority Task")
    print("5. Overdue Tasks")
    print("6. Today's Tasks")
    print("7. Upcoming Tasks")
    view_choice = input("Enter your choice: ")

    if view_choice == "1":
        display_task_list(scheduler.view_tasks())
    elif view_choice == "2":
        display_task_list(scheduler.view_tasks(status=True))
    elif view_choice == "3":
        display_task_list(scheduler.view_tasks(status=False))
    elif view_choice == "4":
        highest_task = scheduler.get_highest_priority_task()
        if highest_task:
            print("Highest Priority Task")
            print(highest_task.display())
        else:
            print("No pending tasks available.")
    elif view_choice == "5":
        print("Overdue Tasks")
        display_task_list(scheduler.get_overdue_tasks())
    elif view_choice == "6":
        print("Today's Tasks")
        display_task_list(scheduler.get_todays_tasks())
    elif view_choice == "7":
        print(f"Upcoming Tasks ({UPCOMING_DAYS} days)")
        display_task_list(scheduler.get_upcoming_tasks())
    else:
        print("Invalid choice.")


def search_menu(scheduler):
    """Handle name, priority, and date-based searching."""
    print("Search Tasks")
    print("1. Search by Name")
    print("2. Search by Priority")
    print("3. Search by Date")
    search_choice = input("Enter your choice: ")

    if search_choice == "1":
        name = input("Enter task name to search: ")
        task = scheduler.search_task(name)
        if task:
            print(task.display())
        else:
            print(f"No task named '{name}' found.")
    elif search_choice == "2":
        priority = prompt_for_priority()
        matching_tasks = scheduler.search_by_priority(priority)
        if not matching_tasks:
            print("No tasks found for that priority.")
        else:
            display_task_list(matching_tasks)
    elif search_choice == "3":
        try:
            due_date_str = input("Enter a date to search (YYYY-MM-DD): ")
            target_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            matching_tasks = scheduler.search_by_date(target_date)
            if not matching_tasks:
                print("No tasks found for that date.")
            else:
                display_task_list(matching_tasks)
        except ValueError:
            print("Invalid date format.")
    else:
        print("Invalid choice.")


def statistics_menu(scheduler):
    """Show statistics, sort tasks, or remove completed tasks."""
    print("Manage Tasks")
    print("1. Show Statistics")
    print("2. Sort Tasks")
    print("3. Delete Completed Tasks")
    manage_choice = input("Enter your choice: ")

    if manage_choice == "1":
        stats = scheduler.get_statistics()
        print(f"Total Tasks: {stats['total']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")
        print(f"Overdue: {stats['overdue']}")
        print(f"Progress: {stats['progress']}% Complete")
    elif manage_choice == "2":
        print("Sort by:")
        print("1. Priority")
        print("2. Due Date")
        print("3. Alphabetically")
        sort_choice = input("Enter your choice: ")
        if sort_choice == "1":
            scheduler.sort_tasks("priority")
        elif sort_choice == "2":
            scheduler.sort_tasks("due_date")
        elif sort_choice == "3":
            scheduler.sort_tasks("alphabetical")
        else:
            print("Invalid sort option.")
            return
        scheduler.save_tasks()
        print("Tasks sorted.")
    elif manage_choice == "3":
        confirmation = input("Are you sure? (Y/N): ").strip().lower()
        if confirmation == "y":
            scheduler.delete_completed_tasks()
            print("Completed tasks removed.")
        else:
            print("Deletion cancelled.")
    else:
        print("Invalid choice.")
