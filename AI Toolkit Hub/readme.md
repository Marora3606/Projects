# AI Toolkit Hub — Multi-Domain Intelligence Platform

A multi-page Streamlit application with user authentication, a SQLite-backed
incident and ticket store, Plotly analytics, and an LLM assistant that works
against OpenAI or any OpenAI-compatible gateway.

Roughly 1,700 lines of Python across `models/`, `services/`, `database/` and
`pages/`.

---

## 🌟 Features

* 🔐 **Authentication** — registration and login with `bcrypt` password hashing
  and JWT session tokens, plus a three-tier role hierarchy (`user` → `analyst` →
  `admin`).
* 🗄️ **SQLite persistence** — `users`, `cyber_incidents`, `it_tickets` and
  `datasets_metadata` tables, seeded from CSV on first run.
* 📊 **Analytics** — Plotly charts over incident severity, ticket volume and
  dataset metadata.
* 💬 **LLM assistant** — domain-scoped chat for cybersecurity, data science and
  IT operations, with a non-streaming fallback on gateway timeouts.
* 🌐 **Configurable API base URL** — works with `api.openai.com`, third-party
  proxies, or a local Ollama endpoint.

---

## 📁 Structure

```text
AI Toolkit Hub/
├── Home.py                     # Entry point: login, registration, overview
├── database/
│   └── db.py                   # SQLite connection helper
├── models/                     # One module per table
│   ├── schema.py               # CREATE TABLE definitions (DDL)
│   ├── users.py                # Parameterised user queries
│   ├── incidents.py
│   ├── tickets.py
│   └── datasets.py
├── services/                   # Business logic, kept out of the UI layer
│   ├── auth_manager.py         # JWT issue / verify / permission checks
│   ├── user_service.py         # Registration, login, bcrypt handling
│   └── ai_assistant.py         # LLM client wrapper
├── pages/                      # Streamlit multi-page UI
│   ├── 1_Dashboard.py
│   ├── 2_Analytics.py
│   ├── 4_Settings.py
│   └── 5_Chatbot.py
├── DATA/                       # Seed CSVs (databases are gitignored)
├── .streamlit/
│   └── secrets.toml.example    # Template — copy to secrets.toml
├── requirements.txt
└── readme.md
```

**Design note:** UI, business logic and data access are deliberately separated.
`pages/` never touches SQL directly — it calls `services/`, which calls
`models/`. Adding a table means adding one module rather than editing the UI.

---

## 🔧 Setup

**1. Install dependencies**

```bash
cd "AI Toolkit Hub"
pip install -r requirements.txt
```

**2. Configure secrets**

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then edit `secrets.toml`:

```toml
OPENAI_API_KEY  = "sk-..."                       # your key
OPENAI_BASE_URL = "https://api.openai.com/v1"    # or a compatible gateway
JWT_SECRET_KEY  = "..."                          # see below
```

Generate a signing key with:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

> `secrets.toml` is gitignored and must never be committed. If `JWT_SECRET_KEY`
> is absent the app still runs — it generates a random key at startup and prints
> a warning — but logins will not survive a restart.

**3. Run**

```bash
streamlit run Home.py
```

Open <http://localhost:8501>. The database and tables are created automatically
on first launch, seeded from the CSVs in `DATA/`.

---

## 🔐 Security notes

- Passwords are hashed with `bcrypt` (salted, deliberately slow) — never stored
  in plain text and never reversible.
- All SQL uses parameterised queries (`?` placeholders), so user input can never
  be interpreted as SQL.
- JWTs are signed with HS256 and verified against an explicit algorithm
  allowlist, which prevents the `alg=none` forgery attack.
- The database is the single source of truth for credentials.

---

## ⚠️ Known limitations

Being honest about what this does and does not do:

- **Streamlit's session model does most of the auth work.** Login state lives in
  `st.session_state`, which is server-side and per-session, so the JWT is closer
  to a demonstration of token handling than a load-bearing security boundary. In
  a client/server architecture the token would carry real weight.
- **No tests.** The auth and permission logic is pure and easily testable; there
  simply are no tests yet.
- **Roles cannot be changed from the UI** — new accounts are always `user`, and
  promotion requires editing the database directly.
- **Positional row indexing.** Queries return tuples accessed by index
  (`user[0]`), which breaks if a column is inserted in the middle.
  `sqlite3.Row` would fix this.
- **No rate limiting** on the LLM endpoint, so nothing prevents a user from
  burning API credits.

---

## ❓ Troubleshooting

| Issue | Cause | Fix |
| :--- | :--- | :--- |
| `401 Invalid API Key` | Proxy key sent to the official OpenAI endpoint | Set `OPENAI_BASE_URL` to your gateway in `secrets.toml` |
| `403 Model Permission Denied` | Key lacks access to the selected model | Pick an accessible model in the Chatbot sidebar |
| Stuck on "Thinking…" / 504 | Gateway latency or a stalled stream | Handled automatically — falls back to non-streaming with a 30s timeout |
| Warning about `JWT_SECRET_KEY` | Not set in secrets or environment | Generate one and add it to `secrets.toml` |
| Logins lost after restart | Random per-run JWT key | Same fix as above |

---

## 👨‍💻 Author

**Manan Arora**
