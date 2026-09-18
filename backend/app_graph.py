from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from backend.graph import build_graph


DB_PATH = "workflow.db"


class GraphRuntime:

    def __init__(self):
        self.checkpointer_context = None
        self.checkpointer = None
        self.graph = None

    async def startup(self):

        self.checkpointer_context = (
            AsyncSqliteSaver.from_conn_string(DB_PATH)
        )

        self.checkpointer = (
            await self.checkpointer_context.__aenter__()
        )

        self.graph = build_graph(
            checkpointer=self.checkpointer
        )

        print("Graph runtime started.")

    async def shutdown(self):

        if self.checkpointer_context:

            await self.checkpointer_context.__aexit__(
                None,
                None,
                None,
            )

        print("Graph runtime stopped.")


runtime = GraphRuntime()