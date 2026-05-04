from langgraph.graph import StateGraph , START, END
from langgraph.prebuilt import ToolNode
from agent.state import AgentState
from agent.nodes import agent_node, should_continue_node, tools


builder = StateGraph(AgentState)

tool_node = ToolNode(tools = tools)

builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent",should_continue_node, {
    "tools": "tools",
    "__end__": END
})
builder.add_edge("tools", "agent")

graph = builder.compile()
