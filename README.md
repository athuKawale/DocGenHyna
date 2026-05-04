# DocGenHyna: Automated Codebase Documentation Agent

DocGenHyna is a powerful, autonomous agent system built with **LangGraph** and **Graphify**. It analyzes your source code, builds a comprehensive structural knowledge graph, and utilizes specialized AI agents to generate professional documentation for your APIs, Architecture, and UI layers.

## 🚀 Features

- **Automated Graph Generation**: Uses the Graphify CLI to build a multi-level knowledge graph of your codebase.
- **Parallel Documentation Agents**: Deploys specialized agents for API, Architecture, and UI documentation that run in parallel.
- **Autonomous Exploration**: Agents utilize Graphify tools to independently query and explain code relationships and data flows.
- **Unified Reporting**: Aggregates all generated documentation into a single consolidated project report.
- **Environment Driven**: Seamlessly switches between models like Anthropic Claude, OpenAI, or local models via Ollama.

## 🛠️ Prerequisites

- **Python 3.10+** (Recommended to use [uv](https://github.com/astral-sh/uv))
- **Graphify**: `pip install graphifyy`
- **Environment Variables**: An Anthropic API key or a running Ollama instance.

## 📥 Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd DocGenHyna
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   ANTHROPIC_API_KEY=your_key_here
   LLM_MODEL=claude-haiku-4-5
   # Optional: OLLAMA_BASE_URL=http://localhost:11434
   ```

4. **Prepare Source Code**:
   Place the codebase you want to analyze into the `./source_code/` directory (or update the path in `src/graph.py`).

## 📖 Usage

Run the documentation pipeline with a single command:

```bash
uv run src/graph.py
```

### What happens under the hood?
1. **Setup Node**: Detects your source code and runs `graphify update` to generate a knowledge graph if it doesn't exist.
2. **Analysis**: Ingests the initial `GRAPH_REPORT.md` to understand high-level communities and "God Nodes".
3. **Parallel Agents**: Three agents start in parallel:
   - **API Agent**: Documents endpoints, services, and state management logic.
   - **Architecture Agent**: Explains module relationships, dependency trees, and system design.
   - **UI Agent**: Analyzes components, hooks, and user interface structure.
4. **Aggregator**: Collects all generated docs, saves them to `./analysis_docs/`, and prints a final summary.

## 📁 Output Structure

- `analysis_docs/`:
  - `API.md`: Detailed API and State documentation.
  - `Architecture.md`: System design and dependency analysis.
  - `UI.md`: Component and interface overview.
- `source_code/graphify-out/`:
  - `graph.json`: The queryable knowledge graph.
  - `graph.html`: An interactive 3D visualization of your code.
  - `GRAPH_REPORT.md`: Initial structural findings.

## 🔧 Extending & Customizing

DocGenHyna is designed to be highly modular. You can easily adapt it to generate different types of documentation (e.g., Security Audits, Database Schemas, Test Coverage):

1. **Modify Prompts**: All agent instructions are centralized in `src/prompt.py`. Update these templates to change the focus or format of the output.
2. **Add New Nodes**: To add a new documentation type, simply define a new `call_llm_X` function in `src/graph.py` and register it in the `parallel_workflow`.
3. **Token Efficiency**: Unlike traditional agents that ingest the entire codebase, DocGenHyna agents use the `GRAPHIFY_TOOLS` to surgically query only the metadata they need. This allows for deep codebase analysis using a fraction of the tokens.

---
Built with ❤️ using LangGraph and Graphify.
