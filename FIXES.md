# Fixes applied — 9 August 2026

Read this alongside the code. Every change below is a **fix to something broken
or unsafe** — no features were added, nothing was refactored, and no project's
behaviour changed except where a bug is described.

Every comment added to the code is tagged `# LEARN:` so you can find them, and
remove them later with:

```bash
grep -v '# LEARN:' path/to/file.py > clean.py
```

---

## ⚠️ ONE THING ONLY YOU CAN DO

**Revoke the OpenAI key in `AI Toolkit Hub/.streamlit/secrets.toml`.**

It was committed to git and your history contains a commit called "git push",
so it has almost certainly been on GitHub. I removed the file from tracking, but
**git history is permanent** — anyone who clones the repo can still recover the
key from an old commit. Untracking prevents future exposure; it does not undo
past exposure.

Go to <https://platform.openai.com/api-keys>, delete that key, create a new one,
and paste it into `secrets.toml` (now gitignored, so it stays local).

Takes two minutes. Until you do it, the key is live and billable to you.

---

## 1. Secrets, credentials and databases removed from git

**Was:** these five files were tracked and pushed.

| File | What was in it |
|---|---|
| `AI Toolkit Hub/.streamlit/secrets.toml` | A working OpenAI API key |
| `AI Toolkit Hub/DATA/users.txt` | Real usernames + bcrypt password hashes |
| `AI Toolkit Hub/app.db` | SQLite database |
| `AI Toolkit Hub/DATA/intelligence_platform.db` | SQLite database |
| `AI Toolkit Hub/database/intelligence_platform.db` | SQLite database |

**Now:** untracked via `git rm --cached` and blocked by `.gitignore`.

**Important:** `--cached` removes the file from *git*, not from *disk*. Every one
of those files is still exactly where it was and your app runs unchanged. Verify
for yourself:

```bash
ls -la "AI Toolkit Hub/.streamlit/secrets.toml"   # still there
git ls-files | grep secrets                        # no output = untracked
```

Added `.streamlit/secrets.toml.example` — a template with empty values, safe to
commit, so anyone cloning knows which keys they need to supply.

---

## 2. Forgeable JWT signing key — `services/auth_manager.py`

**The bug.** The class had a placeholder default that was never overridden:

```python
def __init__(self, secret_key: str = "your-secret-key"):
...
auth_manager = AuthManager()      # <- used the placeholder
```

**Why it mattered.** A JWT is *signed*, not *encrypted*. Anyone can decode one
and read it — paste a token into jwt.io and you'll see the username and role in
plain text. The only thing preventing tampering is the signature, computed from
the payload plus a secret.

With the secret set to a well-known placeholder string, anyone could construct
their own token claiming `{"role": "admin"}`, sign it with that same string, and
`check_permission()` would let them straight through. Your role hierarchy
(`user` → `analyst` → `admin`) was correctly written and completely bypassable.

**The fix.** The key now comes from, in order:

1. `JWT_SECRET_KEY` environment variable
2. `JWT_SECRET_KEY` in `.streamlit/secrets.toml`
3. A cryptographically random key generated fresh at startup, with a printed
   warning

I generated a real key and added it to your `secrets.toml`, so option 2 applies
and you'll see no warning. Option 3 exists so the app still runs for anyone who
clones it without configuring anything — it stays secure, tokens just don't
survive a restart.

**Also fixed here:** `datetime.utcnow()` → `datetime.now(timezone.utc)`. The old
form is deprecated in Python 3.12 and will be removed; it also returned a
*naive* datetime that merely happened to hold UTC, which is a classic source of
off-by-hours bugs.

**Verified:** a token signed with the old `"your-secret-key"` is now rejected.

---

## 3. Password hashes no longer written to a text file — `services/user_service.py`

**Was:** `register_user()` wrote every new credential to the database *and*
appended it to `DATA/users.txt`.

**Why that's wrong:**

- **Two sources of truth.** Delete a user from the database and they still exist
  in the file. Any fact stored in two places will eventually disagree.
- **It was committed to git.** bcrypt is salted and deliberately slow, so those
  hashes aren't trivially crackable — but any weak password in that list can now
  be brute-forced offline, at an attacker's leisure, permanently.
- **No file locking.** Two simultaneous registrations could interleave and
  corrupt a line.

**Now:** the database is the single source of truth. `login_user()` already read
from the database and never from the file, so nothing about login changes.
`migrate_users_from_file()` still exists if you ever need to import the old file
— it just receives no new rows.

---

## 4. Every JWT claimed to be user 1 — `Home.py`

**Was:**

```python
user_id = 1  # In real app, get from database
```

Every user's token said `user_id: 1`, regardless of who logged in. Any future
code that trusted `token["user_id"]` — "show my incidents", "my settings" —
would have shown user 1's data to everyone.

**Now:** the real id is read from the users table.

Note the comment I left there: the code uses positional indexes (`user_row[0]`)
which break if you ever add a column in the middle. `sqlite3.Row` would let you
write `user["id"]` instead. I left that alone to keep the change small — it's a
good thing for you to fix yourself.

---

## 5. Repository size

**Was:** 1.4 GB working tree, 212 MB `.git`.

Untracked from git (still on disk, every project still runs):

- `CrimeScope/27d1328a9d866c8330c411a3a9e5b517314b8bea.zip` — 95 MB
- `CrimeScope/20*/*.csv` — 24 monthly Metropolitan Police files, ~23 MB each
- `SmartChef .../recipes_final.csv` — 26 MB

Tracked file count went from **99 → 68**.

**Why this matters:** GitHub hard-blocks any file over 100 MB, so that zip was
right at the edge. More practically, a reviewer who clicks "clone" waits several
minutes for data they don't want. Many just close the tab.

**Caveat:** this stops *new* commits carrying the data. The existing history
still contains it, so `.git` stays 212 MB until the history is rewritten or the
repo is recreated. See the "still to do" section.

The Metropolitan Police data is public and re-downloadable from
<https://data.police.uk/data/>.

---

## What I deliberately did NOT change

**The two f-string SQL queries.** In `pages/1_Dashboard.py:48` and
`pages/2_Analytics.py:43` you have:

```python
cursor.execute(f"SELECT COUNT(*) FROM {table}")
```

That *looks* like SQL injection, and it's the right instinct to flag it. But
`table` comes from a hardcoded dictionary in the line above, never from user
input, so it isn't exploitable. I left it alone rather than change working code
for no security gain.

Worth knowing for interviews: table and column names genuinely *cannot* be
parameterised — `?` placeholders only work for values. When a table name must be
dynamic, you validate it against an allowlist. Yours effectively is one.

**Everything structural.** No refactoring, no new features, no repo splitting,
no git history rewriting. You asked for fixes only, and rewriting history
requires a force-push that I shouldn't do to your repository without you at the
keyboard.

---

## Still to do — yours

1. **Revoke and replace the OpenAI key** (see the top of this file)
2. Consider **splitting into six repos** so each project can be pinned on GitHub
   independently and nobody clones 1.4 GB to read a 194-line script
3. **Commit more often, in smaller pieces.** 18 commits with 12 on one day, and
   messages like `git push` and `Create readme.md`, reads as "uploaded finished
   work" rather than "built over time"
4. Move the coursework PDFs (`CST1450 Coursework Report.pdf`,
   `Assessment 2 Part A.docx`) out of the project folders, or be upfront that
   those two were academic assignments
5. Replace positional row indexes with `sqlite3.Row` in `Home.py`

---

## Verification run

```
all project .py files compile ......................... OK
register user ......................................... OK
duplicate username blocked ............................ OK
users.txt no longer written on registration ........... OK
login with correct password ........................... OK
login with wrong password rejected .................... OK
JWT round-trip preserves real user_id ................. OK
forged admin token signed with "your-secret-key" ...... REJECTED  ← the fix
role hierarchy (admin>=analyst, user<admin, unknown<user) OK
no secrets / databases / large files tracked .......... OK
```

Backups of every file I edited sit beside the originals as `.bak`, and they're
gitignored:

```
AI Toolkit Hub/Home.py.bak
AI Toolkit Hub/services/auth_manager.py.bak
AI Toolkit Hub/services/user_service.py.bak
```

Diff any of them to see exactly what changed:

```bash
diff "AI Toolkit Hub/services/auth_manager.py.bak" "AI Toolkit Hub/services/auth_manager.py"
```
