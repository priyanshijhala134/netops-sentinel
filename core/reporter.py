from datetime import datetime
import json

def generate_incident_report(
    incident_type,
    cpu_before,
    cpu_after,
    action_taken,
    success
):
    return{
        "timestamp":datetime.now().isoformat(),
        "incident_type": incident_type,
        "cpu_before": cpu_before,
        "cpu_after": cpu_after,
        "action_taken": action_taken,
        "success": success
    }

def save_report(report, path="incidents.log"):
    with open(path, "a") as f:
        f.write(json.dumps(report)+"\n")