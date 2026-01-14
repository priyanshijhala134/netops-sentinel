from typing import TypedDict, Optional
from datetime import datetime
import time
from langgraph.graph import StateGraph, END

# -------- IMPORTS --------
from agents.monitoring_agent import get_avg_cpu
from agents.llm_reasoning import decide_action_llm
from agents.healing_agent import heal
from core.memory import count_recent_fails
from core.reporter import generate_incident_report, save_report
from config.threshold import CPU_HIGH_THRESHOLD

class IncidentState(TypedDict):
    cpu_before: float
    cpu_after: Optional[float]
    decision: Optional[str]
    state: str

# -------- NODES --------

def monitor_node(state: IncidentState):
    cpu = get_avg_cpu()
    print("DEBUG: avg_cpu=", cpu)

    if cpu < CPU_HIGH_THRESHOLD:
        print("SYSTEM: CPU within safe limits, no action required")

    return {
        "cpu_before": cpu,
        "state": "HIGH_CPU" if cpu >= CPU_HIGH_THRESHOLD else "NORMAL"
    }


def decide_node(state: IncidentState):
    fails = count_recent_fails("HIGH_CPU")

    decision = decide_action_llm(
        state=state["state"],
        cpu_before=state["cpu_before"],
        cpu_after=None,
        recent_failures=fails
    )

    for r in decision["reasoning"]:
        print("LLM_REASON:", r)
    return {
        "decision": decision["decision"]
    }


def heal_node(state: IncidentState):

    print("Executing heal action...")
    heal("HIGH_CPU")

    print("Waiting for system stabilization...")
    time.sleep(10) 

    cpu_after = get_avg_cpu()
    print("DEBUG: avg_cpu=", cpu_after)

    return {
        "cpu_after": cpu_after
    }

def escalate_node(state: IncidentState):
    print("Escalation triggered — human intervention required")
    state["escalated"]=True
    return {
        "cpu_after": state["cpu_before"]
    }

def generate_incident_report(
    incident_type,
    cpu_before,
    cpu_after,
    action_taken,
    success,
):
    return {
        "timestamp": datetime.now().isoformat(),
        "incident_type": incident_type,
        "cpu_before": cpu_before,
        "cpu_after": cpu_after,
        "action_taken": action_taken,
        "success": success,
    }

def verify_node(state: IncidentState):
    success = state["cpu_after"] < CPU_HIGH_THRESHOLD

    report = generate_incident_report(
        incident_type="HIGH_CPU",
        cpu_before=state["cpu_before"],
        cpu_after=state["cpu_after"],
        action_taken=state["decision"],
        success=success,
    )

    save_report(report)
    print("Incident report saved")

    return {}


# -------- GRAPH --------

graph = StateGraph(IncidentState)

graph.add_node("monitor", monitor_node)
graph.add_node("decide", decide_node)
graph.add_node("heal", heal_node)
graph.add_node("escalate", escalate_node)
graph.add_node("verify", verify_node)

graph.set_entry_point("monitor")

graph.add_edge("monitor", "decide")

graph.add_conditional_edges(
    "decide",
    lambda s: s["decision"],
    {
        "heal": "heal",
        "escalate": "escalate",
        "do_nothing": END
    }
)

graph.add_edge("heal", "verify")
graph.add_edge("escalate", "verify")
graph.add_edge("verify", END)

incident_graph = graph.compile()

