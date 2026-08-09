# =============================================================
# Module: task.py
# Project Area: DayFlow
# Purpose: Implements the runtime logic for this project component.
# Notes: Keep this file focused on one responsibility so future
# maintenance remains straightforward.
# =============================================================

from datetime import datetime

PRIORITY_NAMES = {
    1: "Highest",
    2: "High",
    3: "Medium",
    4: "Low",
    5: "Lowest",
}


class Task:
    """Represents a single task with a priority, due date, and completion status."""

    def __init__(self, name, priority, due_date, completed=False):
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    @property
    def priority_name(self):
        """Return the human-readable priority label."""
        return PRIORITY_NAMES.get(self.priority, "Unknown")

    @property
    def status(self):
        """Return the task status as a label."""
        return "Completed" if self.completed else "Pending"

    def display(self):
        """Return a formatted string representation of the task."""
        return (
            "----------------------------------------\n"
            f"Task: {self.name}\n"
            f"Priority: {self.priority_name}\n"
            f"Due Date: {self.due_date.strftime('%d %b %Y %I:%M %p')}\n"
            f"Status: {self.status}\n"
            "----------------------------------------"
        )

    def to_dict(self):
        """Convert the task to a dictionary for JSON storage."""
        return {
            "name": self.name,
            "priority": self.priority,
            "due_date": self.due_date.isoformat(),
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a task instance from stored dictionary data."""
        return cls(
            name=data["name"],
            priority=data["priority"],
            due_date=datetime.fromisoformat(data["due_date"]),
            completed=data.get("completed", False),
        )
