# DayFlow — Task Scheduler & Daily Planner

A command-line task manager with priorities, categories, due dates and JSON
persistence. Standard library only.

Small, but the most cleanly separated codebase in this workspace — the task
model, the scheduling logic, the menu and the helpers each live in their own
module, and none of them reach into the others' concerns.

---

## 🌟 What it does

* 📝 **Task management** — add, edit, view, search and remove tasks.
* 🎯 **Priorities and categories** — `High` / `Medium` / `Low`, and `Work`,
  `Personal`, `Health`, `Study`.
* 📅 **Due dates and status** — `Pending`, `In Progress`, `Completed`, with date
  validation on input.
* 🔍 **Search and filter** — by title, category, priority or status.
* 💾 **JSON persistence** — everything is written to `tasks.json`, so state
  survives between runs.
* ⚡ **No dependencies** — `json`, `datetime`, `os`, `typing` only.

---

## 📁 Structure

```text
DayFlow/
├── main.py            # Entry point
├── menu.py            # CLI menu handlers and user interaction
├── scheduler.py       # TaskScheduler: task collection + JSON load/save
├── task.py            # Task class
├── utils.py           # Date validation and formatting helpers
├── tasks.json         # Data store (created on first run)
├── requirements.txt   # (standard library only)
└── README.md
```

**Design note:** the separation is the point. `task.py` knows what a task *is*.
`scheduler.py` knows how a collection of tasks is stored and queried. `menu.py`
knows how to talk to a human. Swapping the CLI for a web UI would mean replacing
`menu.py` and nothing else — that is what separation of concerns buys you.

---

## 🔧 Setup

```bash
cd DayFlow
python main.py
```

Requires **Python 3.8+**. Nothing to install.

---

## ⚠️ Known limitations

- **Rewrites the whole JSON file on every change.** Fine for hundreds of tasks,
  poor beyond that, and a crash mid-write can corrupt the file. Writing to a
  temp file and atomically renaming would make saves crash-safe.
- **No concurrency handling.** Two instances running at once will overwrite each
  other's changes.
- **No undo.** Deletions are immediate and permanent.
- **No recurring tasks** — every task is a one-off.
- **No tests.** `scheduler.py` is pure logic over in-memory data and would be
  easy to cover.

---

## 👨‍💻 Author

**Manan Arora**
