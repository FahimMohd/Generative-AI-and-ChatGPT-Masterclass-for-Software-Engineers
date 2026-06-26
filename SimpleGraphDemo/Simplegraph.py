# Simple Langgraph with 3 nodes and a decision edge
from typing_extensions import TypedDict
from typing import Literal
import random
from langgraph.graph import StateGraph, START, END
from IPython.display import Image

class state(TypedDict):
    graph_state : str

def node_1(state):
    print("Node 1")
    return {"graph_state": state["graph_state"] + ": 1"}

def node_2(state):
    print("Node 2")
    return {"graph_state": state["graph_state"] + ": 2"}

def node_3(state):
    print("Node 3")
    return {"graph_state": state["graph_state"] + ": 3"}

# Decision edge

def decision_edge(state) -> Literal ["node_2","node_3"]:
    print("Decision edge")

    if random.random() < 0.5:
        return "node_2"
    else:
        return "node_3"
    
# Define the graph

graph = StateGraph(state)
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
graph.add_node("node_3", node_3)

#logic for edge

graph.add_edge(START, "node_1")
graph.add_conditional_edges("node_1", decision_edge)
graph.add_edge("node_2", END)
graph.add_edge("node_3", END)

#compile graph

graphOutput = graph.compile()

mermaid_image = Image(graphOutput.get_graph().draw_mermaid_png())

with open("simplegraph.png", "wb") as file:
    file.write(mermaid_image.data)

tempgraph = graphOutput.invoke({"graph_state": "Please show a number starting from 1.."})
print(tempgraph)