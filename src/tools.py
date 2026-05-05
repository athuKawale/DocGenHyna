import os
import subprocess
from langchain_core.tools import tool

# Load from environment variable, default to the graphify-out inside source_code
GRAPH_PATH = os.getenv("GRAPH_PATH", "./source_code/graphify-out/graph.json")

# Use graphify from activated venv
GRAPHIFY_BIN = "graphify"

def run_graphify_cmd(args: list[str]) -> str:
    """Helper to run graphify CLI commands."""
    try:
        result = subprocess.run(
            [GRAPHIFY_BIN, *args],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            return f"Error running graphify: {result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"Execution error: {str(e)}"

@tool
def graphify_query(question: str) -> str:
    """
    Use this tool to ask high-level architectural questions about the codebase.
    It searches the knowledge graph to find relationships, data flows, and module purposes.
    Example questions: "How does authentication work?", "What classes depend on the Database layer?"
    """
    return run_graphify_cmd(["query", question, "--graph", GRAPH_PATH])

@tool
def graphify_explain(node_name: str) -> str:
    """
    Use this tool to get a detailed explanation of a specific class, function, or component.
    It returns the component's purpose, its community, and all files/classes it interacts with.
    Example: graphify_explain("PlaybackFragment")
    """
    return run_graphify_cmd(["explain", node_name, "--graph", GRAPH_PATH])

@tool
def graphify_path(source_node: str, target_node: str) -> str:
    """
    Use this tool to find how two different components are connected in the codebase.
    It returns the shortest execution path or dependency chain between them.
    Example: graphify_path("LoginScreen", "UserRepository")
    """
    return run_graphify_cmd(["path", source_node, target_node, "--graph", GRAPH_PATH])

# List of tools to provide to your agent
GRAPHIFY_TOOLS = [graphify_query, graphify_explain, graphify_path]
