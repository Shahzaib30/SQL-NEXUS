import json
import uuid
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from tools.db_tools import get_all_tables, get_table_schema, execute_read_query

tools = [get_all_tables, get_table_schema, execute_read_query]


