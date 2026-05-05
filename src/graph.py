from typing import TypedDict, Dict, Annotated
import operator
from langgraph.graph import StateGraph, MessagesState, START, END
from dotenv import load_dotenv
from langchain.agents import create_agent
from chat_model import chat_model
from prompt import llm_call_1, llm_call_2, llm_call_3
from tools import GRAPHIFY_TOOLS
from IPython.display import Image, display
import os

# Load environment variables first
load_dotenv()

from langfuse.langchain import CallbackHandler
from langfuse import Langfuse

_langfuse = Langfuse()

def get_langfuse_handler(session_id=None, tags=None, trace_name=None):
    h = CallbackHandler()
    if session_id: h.session_id = session_id
    if tags: h.tags = tags
    if trace_name: h.trace_name = trace_name
    return h

llm = chat_model()

# Graph state
class State(TypedDict):
    source_type: str                      # "android" | "figma" | "backend"
    source_path: str                      # /path/to/source/repo

    graph_path: str                       # path to graphify-out/graph.json
    graph_report: str                     # content of GRAPH_REPORT.md

    analysis_docs:      Annotated[Dict[str, str], operator.ior]    # {"UI.md": "...", "API.md": "...", ...}
    analysis_doc_paths: Dict[str, str]    # {"UI.md": "/out/UI.md", ...}
    retrigger_node: str                   # Node to re-trigger if validation fails


# Nodes
def setup_state(state: State):
    """Initialize source path, analysis document paths, and run graphify if needed"""
    import subprocess
    
    source_path = state.get("source_path", "./source_code/")
    graph_out_dir = os.path.join(source_path, "graphify-out")
    graph_json_path = os.path.join(graph_out_dir, "graph.json")
    report_path = os.path.join(graph_out_dir, "GRAPH_REPORT.md")
    
    # Set the environment variable for tools.py
    os.environ["GRAPH_PATH"] = graph_json_path
    
    # Run graphify if the output directory doesn't exist
    if not os.path.exists(graph_out_dir):
        print(f"Graphify output not found. Running graphify on {source_path}...")
        try:
            subprocess.run(["uv", "run", "graphify", "update", source_path], check=True)
        except Exception as e:
            print(f"Error running graphify: {e}")
            
    # Read the graph report if it exists
    graph_report = "No graph report available."
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            graph_report = f.read()
            
    return {
        "source_path": source_path,
        "graph_path": graph_json_path,
        "graph_report": graph_report,
        "source_type": state.get("source_type", "Android Codebase"),
        "analysis_doc_paths": {
            "API.md": "./analysis_docs/API.md",
            "Architecture.md": "./analysis_docs/Architecture.md",
            "UI.md": "./analysis_docs/UI.md"
        },
        "analysis_docs": {}
    }


def call_llm_1(state: State):
    """Agent node to generate API documentation"""
    
    # Create Langfuse handler for this agent
    langfuse_handler = get_langfuse_handler(
        session_id=f"analysis-{state.get('source_type', 'unknown')}",
        tags=["api-documentation", state.get("source_type", "unknown")],
        trace_name="generate-api-documentation"
    )

    agent = create_agent(
        model=llm,
        tools=GRAPHIFY_TOOLS,
        system_prompt=llm_call_1.format(
            source_type=state.get("source_type", "unknown"),
            source_path=state.get("source_path", "./source_code/"),
            graph_report=state.get("graph_report", "No graph report available.")
        ),
        name="API.md"
    )

    result = agent.invoke(
        {"messages": [("user", "Please generate the API.md documentation now.")]},
        config={"callbacks": [langfuse_handler]}
    )
    
    return {"analysis_docs": {"API.md": result["messages"][-1].content}}


def call_llm_2(state: State):
    """Agent node to generate Architecture documentation"""
    
    # Create Langfuse handler for this agent
    langfuse_handler = get_langfuse_handler(
        session_id=f"analysis-{state.get('source_type', 'unknown')}",
        tags=["architecture-documentation", state.get("source_type", "unknown")],
        trace_name="generate-architecture-documentation"
    )

    agent = create_agent(
        model=llm,
        tools=GRAPHIFY_TOOLS,
        system_prompt=llm_call_2.format(
            source_type=state.get("source_type", "unknown"),
            source_path=state.get("source_path", "./source_code/"),
            graph_report=state.get("graph_report", "No graph report available.")
        ),
        name="Architecture.md"
    )

    result = agent.invoke(
        {"messages": [("user", "Please generate the Architecture.md documentation now.")]},
        config={"callbacks": [langfuse_handler]}
    )
    
    return {"analysis_docs": {"Architecture.md": result["messages"][-1].content}}


def call_llm_3(state: State):
    """Agent node to generate UI documentation"""
    
    # Create Langfuse handler for this agent
    langfuse_handler = get_langfuse_handler(
        session_id=f"analysis-{state.get('source_type', 'unknown')}",
        tags=["ui-documentation", state.get("source_type", "unknown")],
        trace_name="generate-ui-documentation"
    )

    agent = create_agent(
        model=llm,
        tools=GRAPHIFY_TOOLS,
        system_prompt=llm_call_3.format(
            source_type=state.get("source_type", "unknown"),
            source_path=state.get("source_path", "./source_code/"),
            graph_report=state.get("graph_report", "No graph report available.")
        ),
        name="UI.md"
    )

    result = agent.invoke(
        {"messages": [("user", "Please generate the UI.md documentation now.")]},
        config={"callbacks": [langfuse_handler]}
    )
    
    return {"analysis_docs": {"UI.md": result["messages"][-1].content}}


def aggregator(state: State):
    """Combine analysis docs and verify they were generated correctly"""
    analysis_docs = state.get("analysis_docs", {})
    doc_paths = state.get("analysis_doc_paths", {})

    # Write individual docs to disk (save whatever we have so far)
    os.makedirs("./analysis_docs/", exist_ok=True)
    for filename, path in doc_paths.items():
        if filename in analysis_docs and analysis_docs[filename]:
            with open(path, "w") as f:
                f.write(analysis_docs[filename])
            print(f"Saved: {path}")

    # Verify all expected documents exist and are not empty
    missing_docs = [name for name in doc_paths if not analysis_docs.get(name)]
    
    if missing_docs:
        print(f"Validation failed. Missing or empty docs: {missing_docs}")
        # In a more complex graph, we could use this to route back to agents
        return {"retrigger_node": "call_llm_1"} # Example signal

    # Combine all docs into a single final report
    combined_report = "# Project Analysis Report\n\n"
    for filename, content in analysis_docs.items():
        combined_report += f"## {filename}\n\n{content}\n\n"
        
    return {"graph_report": combined_report, "retrigger_node": "none"}
    
    


# Build workflow
builder = StateGraph(State)

# Add nodes
builder.add_node("setup_state", setup_state)
builder.add_node("call_llm_1", call_llm_1)
builder.add_node("call_llm_2", call_llm_2)
builder.add_node("call_llm_3", call_llm_3)
builder.add_node("aggregator", aggregator)

# Add edges to connect nodes
builder.add_edge(START, "setup_state")
builder.add_edge("setup_state", "call_llm_1")
builder.add_edge("setup_state", "call_llm_2")
builder.add_edge("setup_state", "call_llm_3")
builder.add_edge("call_llm_1", "aggregator")
builder.add_edge("call_llm_2", "aggregator")
builder.add_edge("call_llm_3", "aggregator")
builder.add_edge("aggregator", END)
parallel_workflow = builder.compile()

# Show workflow
#display(Image(parallel_workflow.get_graph().draw_mermaid_png()))


# save this image
# with open("workflow.png", "wb") as f:
#     f.write(parallel_workflow.get_graph().draw_mermaid_png())

# Invoke
state = parallel_workflow.invoke({"source_type": "backend", "source_path": "./source_code/"})
print("\nFinal Graph Report Summary:")
print(state.get("graph_report", "No report generated."))

# Flush Langfuse traces before exit
_langfuse.flush()