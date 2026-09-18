import sqlite3
from datetime import datetime, timezone

DB_PATH = "moderator.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_moderator_table():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS moderator_requests (
            request_id TEXT PRIMARY KEY,
            thread_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            question TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    columns = {
        row[1]
        for row in connection.execute(
            "PRAGMA table_info(moderator_requests)"
        )
    }

    if "request_id" not in columns:
        connection.execute(
            "ALTER TABLE moderator_requests "
            "ADD COLUMN request_id TEXT"
        )

    connection.commit()
    connection.close()


def add_moderator_request(
    request_id,
    thread_id,
    user_id,
    question,
    reason,
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO moderator_requests
        (
            request_id,
            thread_id,
            user_id,
            question,
            reason,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            request_id,
            thread_id,
            user_id,
            question,
            reason,
            "pending",
            datetime.now(timezone.utc).isoformat(),
        ),
    )

    connection.commit()
    connection.close()


def get_pending_requests():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            request_id,
            thread_id,
            user_id,
            question,
            reason,
            status,
            created_at
        FROM moderator_requests
        WHERE status = 'pending'
        ORDER BY created_at ASC
        """
    ).fetchall()

    connection.close()

    return [
        {
            "request_id": row[0],
            "thread_id": row[1],
            "user_id": row[2],
            "question": row[3],
            "reason": row[4],
            "status": row[5],
            "created_at": row[6],
        }
        for row in rows
    ]


def complete_request(thread_id, status):
    connection = get_connection()

    connection.execute(
        """
        UPDATE moderator_requests
        SET status = ?
        WHERE thread_id = ?
        """,
        (status, thread_id),
    )

    connection.commit()
    connection.close()


init_moderator_table()