from datetime import datetime, timedelta
import json
from pathlib import Path

from task import Task

UPCOMING_DAYS = 7


class TaskScheduler:
    """Manage a collection of tasks, including loading, saving, searching, and filtering."""

    def __init__(self, storage_file=None):
        self.storage_file = Path(storage_file or Path(__file__).with_name("tasks.json"))
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from disk if the storage file exists."""
        if not self.storage_file.exists():
            return []

        try:
            with self.storage_file.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            return [Task.from_dict(task_data) for task_data in data]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def save_tasks(self):
        """Persist the current task list to disk."""
        with self.storage_file.open("w", encoding="utf-8") as handle:
            json.dump([task.to_dict() for task in self.tasks], handle, indent=2)

    def _normalize_name(self, task_name):
        """Return a normalized version of a task name for case-insensitive comparisons."""
        return task_name.strip().lower()

    def _find_task(self, task_name):
        """Find a task by name using case-insensitive matching."""
        target_name = self._normalize_name(task_name)
        for task in self.tasks:
            if self._normalize_name(task.name) == target_name:
                return task
        return None

    def add_task(self, name, priority, due_date, completed=False):
        """Add a new task if no task with the same name already exists."""
        if self._find_task(name):
            return False

        task = Task(name.strip(), priority, due_date, completed)
        self.tasks.append(task)
        self.sort_tasks("priority")
        self.save_tasks()
        return True

    def remove_task(self, task_name):
        """Remove a task by name."""
        task = self._find_task(task_name)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False

    def edit_task(self, task_name, field, new_value):
        """Edit a task field such as name, priority, or due date."""
        task = self._find_task(task_name)
        if not task:
            return False

        if field == "name":
            new_name = new_value.strip()
            if not new_name:
                return False
            if self._find_task(new_name) and self._normalize_name(new_name) != self._normalize_name(task.name):
                return False
            task.name = new_name
        elif field == "priority":
            task.priority = int(new_value)
        elif field == "due_date":
            task.due_date = new_value
        elif field == "completed":
            task.completed = bool(new_value)
        else:
            return False

        self.sort_tasks("priority")
        self.save_tasks()
        return True

    def sort_tasks(self, sort_option="priority"):
        """Sort tasks using the selected order."""
        if sort_option == "due_date":
            self.tasks.sort(key=lambda task: (task.due_date, task.priority, task.name.lower()))
        elif sort_option == "alphabetical":
            self.tasks.sort(key=lambda task: (task.name.lower(), task.due_date, task.priority))
        else:
            self.tasks.sort(key=lambda task: (task.priority, task.due_date, task.name.lower()))

    def search_task(self, task_name):
        """Search for a task by name."""
        return self._find_task(task_name)

    def view_tasks(self, status=None):
        """Return a filtered list of tasks based on completion state."""
        if status is None:
            return list(self.tasks)
        return [task for task in self.tasks if task.completed == status]

    def get_overdue_tasks(self):
        """Return tasks that are overdue and still pending."""
        today = datetime.now()
        return [task for task in self.tasks if not task.completed and task.due_date < today]

    def get_todays_tasks(self):
        """Return pending tasks due today."""
        today = datetime.now().date()
        return [task for task in self.tasks if not task.completed and task.due_date.date() == today]

    def get_upcoming_tasks(self, days=UPCOMING_DAYS):
        """Return pending tasks due within the next number of days."""
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        return [
            task
            for task in self.tasks
            if not task.completed and today <= task.due_date.date() <= end_date
        ]

    def get_highest_priority_task(self):
        """Return the highest-priority pending task."""
        pending_tasks = [task for task in self.tasks if not task.completed]
        if not pending_tasks:
            return None
        return min(pending_tasks, key=lambda task: (task.priority, task.due_date))

    def search_by_priority(self, priority):
        """Return tasks matching the given priority value."""
        return [task for task in self.tasks if task.priority == priority]

    def search_by_date(self, target_date):
        """Return tasks due on the given date."""
        return [task for task in self.tasks if task.due_date.date() == target_date]

    def get_statistics(self):
        """Return summary statistics for the current task list."""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        overdue = sum(1 for task in self.get_overdue_tasks())
        progress = round((completed / total) * 100) if total else 0
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "progress": progress,
        }

    def mark_completed(self, task_name):
        """Mark a task as completed by name."""
        task = self._find_task(task_name)
        if not task:
            return False
        task.completed = True
        self.save_tasks()
        return True

    def delete_completed_tasks(self):
        """Remove every completed task from the task list."""
        self.tasks = [task for task in self.tasks if not task.completed]
        self.save_tasks()
