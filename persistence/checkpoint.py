from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

DB_PATH = "workflow.db"


def get_checkpointer():
    return AsyncSqliteSaver.from_conn_string(DB_PATH)