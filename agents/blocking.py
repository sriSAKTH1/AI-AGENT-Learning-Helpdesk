import sqlite3
from datetime import datetime, timedelta, timezone


DB_PATH = "user_blocks.db"


def init_block_table():

    connection = sqlite3.connect(DB_PATH)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS user_blocks (
            user_id TEXT PRIMARY KEY,
            blocked_until TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def block_user(user_id: str):

    blocked_until = (
        datetime.now(timezone.utc)
        + timedelta(hours=1)
    )

    connection = sqlite3.connect(DB_PATH)

    connection.execute(
        """
        INSERT OR REPLACE INTO user_blocks
        (user_id, blocked_until)
        VALUES (?, ?)
        """,
        (
            user_id,
            blocked_until.isoformat(),
        ),
    )

    connection.commit()
    connection.close()

    return blocked_until


def is_user_blocked(user_id: str):

    connection = sqlite3.connect(DB_PATH)

    row = connection.execute(
        """
        SELECT blocked_until
        FROM user_blocks
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return False

    blocked_until = datetime.fromisoformat(row[0])

    if datetime.now(timezone.utc) >= blocked_until:

        unblock_user(user_id)

        return False

    return True


def get_blocked_until(user_id: str):

    connection = sqlite3.connect(DB_PATH)

    row = connection.execute(
        """
        SELECT blocked_until
        FROM user_blocks
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return datetime.fromisoformat(row[0])


def unblock_user(user_id: str):

    connection = sqlite3.connect(DB_PATH)

    connection.execute(
        """
        DELETE FROM user_blocks
        WHERE user_id = ?
        """,
        (user_id,),
    )

    connection.commit()
    connection.close()


init_block_table()