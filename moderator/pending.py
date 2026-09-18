import sqlite3
from datetime import datetime, timezone

DB_PATH = "workflow.db"


def init_moderator_table():

    connection = sqlite3.connect(DB_PATH)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS moderator_requests (
            thread_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            question TEXT NOT NULL,
            reason TEXT NOT NULL,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def add_moderator_request(
    thread_id: str,
    user_id: str,
    question: str,
    reason: str
):

    connection = sqlite3.connect(DB_PATH)

    connection.execute(
        """
        INSERT OR REPLACE INTO moderator_requests
        (
            thread_id,
            user_id,
            question,
            reason,
            created_at,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            thread_id,
            user_id,
            question,
            reason,
            datetime.now(timezone.utc).isoformat(),
            "pending",
        ),
    )

    connection.commit()
    connection.close()


def get_pending_requests():

    connection = sqlite3.connect(DB_PATH)

    rows = connection.execute(
        """
        SELECT
            thread_id,
            user_id,
            question,
            reason,
            created_at
        FROM moderator_requests
        WHERE status = 'pending'
        ORDER BY created_at ASC
        """
    ).fetchall()

    connection.close()

    return [
        {
            "thread_id": row[0],
            "user_id": row[1],
            "question": row[2],
            "reason": row[3],
            "created_at": row[4],
        }
        for row in rows
    ]


def complete_moderator_request(
    thread_id: str,
    status: str
):

    connection = sqlite3.connect(DB_PATH)

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