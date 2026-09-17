from langgraph.graph import StateGraph, START, END
from app.ai.state import ComplaintState
from app.ai.nodes.extract import extract_node
from app.ai.nodes.completeness import completeness_node
from app.ai.nodes.risk import risk_node

def build_graph():
    graph = StateGraph(ComplaintState)
    graph.add_node("extract_complaint", extract_node)
    graph.add_node("check_completeness", completeness_node)
    graph.add_node("risk_assessment", risk_node)
    graph.add_edge(START, "extract_complaint")
    graph.add_edge("extract_complaint", "check_completeness")
    graph.add_edge("check_completeness", "risk_assessment")
    graph.add_edge("risk_assessment", END)
    return graph.compile()

complaint_graph = build_graph()

def run_graph(source_text: str):
    return complaint_graph.invoke({"source_text": source_text, "messages": []})
