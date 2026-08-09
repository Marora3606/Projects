# =============================================================
# Module: main.py
# Project Area: DayFlow
# Purpose: Implements the runtime logic for this project component.
# Notes: Keep this file focused on one responsibility so future
# maintenance remains straightforward.
# =============================================================

from menu import (
    add_task_menu,
    edit_task_menu,
    remove_task_menu,
    search_menu,
    statistics_menu,
    view_tasks_menu,
)
from scheduler import TaskScheduler


def main():
    """Run the task manager interactive menu loop."""
    scheduler = TaskScheduler()

    while True:
        print("\n" + "=" * 24 + " TASK MANAGER " + "=" * 24)
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Edit Task")
        print("4. View Tasks")
        print("5. Search Tasks")
        print("6. Manage Tasks")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task_menu(scheduler)
        elif choice == "2":
            remove_task_menu(scheduler)
        elif choice == "3":
            edit_task_menu(scheduler)
        elif choice == "4":
            view_tasks_menu(scheduler)
        elif choice == "5":
            search_menu(scheduler)
        elif choice == "6":
            statistics_menu(scheduler)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid choice from the menu.")


if __name__ == "__main__":
    main()
