# Langgraph to build arithmetic AI agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, START, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image
from langgraph.checkpoint.memory import MemorySaver

def multiply (a, b):
    """Multiply two numbers"""
    return a * b

def add (a, b):
    """Add two numbers"""
    return a + b

def divide (a, b):
    """Divide two numbers"""
    return a / b


tools = [multiply, add, divide]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

system_message = SystemMessage("Hello, I am an AI agent that can perform arithmetic operations. What would you like me to do?")

#node

def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([system_message] + state["messages"])]}

# graph

builder = StateGraph(MessagesState)

#Define nodes

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

#Define edges
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant",tools_condition)
builder.add_edge("tools", "assistant")

#react_graph = builder.compile()

memory = MemorySaver()

# Specify a thread
thread_id = "1"
config = {"configurable": {"thread_id": thread_id}}
react_graph = builder.compile(checkpointer=memory)

mermaid_image = Image(react_graph.get_graph().draw_mermaid_png())

with open("arithmetic.png", "wb") as f:
    f.write(mermaid_image.data)

#input
messages = [HumanMessage(content="What is 2 times 3?")]

#run graph

messages = react_graph.invoke({"messages": messages}, config)

for m in messages['messages']:
    m.pretty_print()

messages = [HumanMessage(content="Add 4 to it")]

#run graph

messages = react_graph.invoke({"messages": messages}, config)

for m in messages['messages']:
    m.pretty_print()