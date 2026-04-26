# SQL Nexus: Local Agentic Text-to-SQL Platform

![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_Agents-blue)
![Qwen](https://img.shields.io/badge/Local_AI-Qwen_2.5_Coder-orange)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791)
![Next.js](https://img.shields.io/badge/Frontend-Next.js-black)

**SQL Nexus** is a privacy-first, fully autonomous Database Agent built with LangGraph and local LLMs. It translates natural language questions into safe, executable PostgreSQL queries, retrieves the data, and summarizes the results in plain English.

Unlike basic LLM wrappers, this project utilizes **Cyclic Graph Orchestration (ReAct pattern)**, giving the AI the autonomy to select tools, fix its own JSON outputs, and execute complex database interactions without hallucinating or breaking conversational memory.

## ✨ Core Features
* **100% Local & Private:** Powered by `qwen2.5-coder:7b` via Ollama. No data is sent to OpenAI or third-party APIs.
* **Agentic Reasoning:** Uses LangGraph to create a cyclic "Agent ↔ Tool" loop. The AI decides when to query the DB and when to speak to the user.
* **Resilient Tool Calling:** Includes custom interceptors to handle raw JSON string outputs and convert them into native LangChain tool calls.
* **Long-Term Memory:** Maintains conversation state, allowing users to ask follow-up questions about recently fetched data.
* **Monorepo Architecture:** Clean separation between the Python/LangGraph backend and the React/Next.js frontend interface.

## 🛠 Tech Stack
**Backend:**
* Python 3.10+
* [LangGraph](https://python.langchain.com/v0.1/docs/langgraph/) (State orchestration)
* [LangChain](https://python.langchain.com/) (Tool binding & wrappers)
* [Ollama](https://ollama.com/) (`qwen2.5-coder:7b` model)
* PostgreSQL & `psycopg2` (Database engine)

**Frontend:**
* Next.js 14+ 
* Tailwind CSS
* Framer Motion (for chat animations)

---

## 🚀 Getting Started

### Prerequisites
1. **PostgreSQL** installed and running.
2. **Ollama** installed. Pull the model by running: 
   ```bash
   ollama pull qwen2.5-coder:7b