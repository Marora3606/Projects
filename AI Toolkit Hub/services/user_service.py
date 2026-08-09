# =============================================================
# Module: user_service.py
# Project Area: AI Toolkit Hub
# Purpose: Implements the runtime logic for this project component.
# Notes: Keep this file focused on one responsibility so future
# maintenance remains straightforward.
# =============================================================

import bcrypt
from pathlib import Path
from database.db import connect_database
from models.users import get_user_by_username, insert_user
from models.schema import create_users_table


def register_user(username, password, role='user'):
    # First check against the current database to avoid duplicate login identities.
    user_exists = get_user_by_username(username)
    if user_exists:
        return False, f"Username '{username}' already exists."

    # Hash the password before persisting so the credential is not stored in plain text.
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Insert into the SQL-backed user table for runtime authentication.
    insert_user(username, password_hash, role)

    # =========================================================================
    # LEARN: REMOVED — this function used to ALSO append every new credential
    # to DATA/users.txt:
    #
    #     with open(users_file, 'a') as f:
    #         f.write(f"{username},{password_hash}\n")
    #
    # Three problems with that:
    #   1. Two sources of truth. The database and the text file could disagree
    #      — delete a user from one and they still exist in the other. Any time
    #      the same fact is stored in two places, they WILL drift apart.
    #   2. The file was committed to git, so real usernames and bcrypt hashes
    #      were published. bcrypt is slow and salted, so the hashes are not
    #      trivially crackable — but weak passwords in that list are now
    #      brute-forceable offline, at the attacker's leisure, forever.
    #   3. No file locking. Two simultaneous registrations could interleave and
    #      corrupt a line.
    #
    # The database is now the single source of truth. Nothing else changes:
    # login_user() already read from the database, never from this file.
    # migrate_users_from_file() below still exists to import the OLD file if
    # you need to — it just is not fed any new rows.
    # =========================================================================

    return True, f"User '{username}' registered successfully!"


def login_user(username, password):
    # Load the account row from the user table to evaluate the supplied credential.
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]
    role = user[3]
    # Compare the submitted passphrase to the stored bcrypt hash inside the model.
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, role
    else:
        return False, "Incorrect password."


def migrate_users_from_file(filepath='DATA/users.txt'):
    # Resolve the input path and stop early when the legacy data source is absent.
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return 0

    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0

    # Read the legacy CSV-style credentials file one line at a time.
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                try:
                    # Insert the account only when there is no duplicate user name.
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except Exception as e:
                    print(f"Error migrating {username}: {e}")

    conn.commit()
    conn.close()
    print(f" Migrated {migrated_count} users")
    return migrated_count
