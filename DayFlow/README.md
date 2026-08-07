# DayFlow - Task Scheduler & Daily Planner

A Python command-line task scheduling and productivity management application that helps users organize, prioritize, and track daily tasks.

---

## 🌟 Key Features

* 📝 **Task Management:** Add, edit, view, search, and remove daily tasks.
* 🎯 **Priority & Category Scoping:** Classify tasks by priority (`High`, `Medium`, `Low`) and category (`Work`, `Personal`, `Health`, `Study`, etc.).
* 📅 **DueDate & Status Tracking:** Assign due dates and track completion status (`Pending`, `In Progress`, `Completed`).
* 🔍 **Search & Filtering:** Search tasks by title, category, priority, or status.
* 💾 **JSON Persistence:** Automatically persists task data to `tasks.json` so data survives between sessions.
* ⚡ **Zero External Dependencies:** Built entirely using Python 3 standard library modules.

---

## 📁 Project Structure

```text
DayFlow/
├── main.py              # CLI Menu entry point
├── menu.py              # User interface menu handlers
├── scheduler.py         # TaskScheduler logic and JSON persistence
├── task.py              # Task class model definition
├── utils.py             # Date validation & formatting helpers
├── tasks.json           # JSON data storage
├── requirements.txt     # Dependency notice (Standard Library)
└── README.md            # Project documentation
```

---

## 🛠️ Setup & Execution

1. **Prerequisites:**
   Python 3.8+ (No external third-party packages required).

2. **Run the Application:**
   ```bash
   python main.py
   ```

---

## 📋 Requirements (`requirements.txt`)

This project relies exclusively on standard Python modules (`json`, `datetime`, `os`, `typing`). No `pip install` steps are necessary.

---

## 👨‍💻 Author

**Manan Arora**
