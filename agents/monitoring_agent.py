import sys
import os

# Get the path to 'netops-sentinel' (two levels up)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the system path so we can import 'core'
sys.path.append(project_root)

from core.incident import Incident
# monitoring logic
CPU_THRESHOLD=85
LATENCY_THRESHOLD=300
DB_CONN_THRESHOLD=90

class MonitoringAgent:
    def defect(self,metrics:dict)->Incident|None:
        if metrics["cpu"]>CPU_THRESHOLD:
            incident=Incident(
                incident_type="HIGH_CPU",
                metrics_snapshot=metrics
            )
            incident.log_event("High cpu detected")
            return incident
        
        if metrics["latency"]>LATENCY_THRESHOLD:
            incident=Incident(
                incident_type="HIGH_LATENCY",
                metrics_snapshot=metrics
            )
            incident.log_event("High latency detected")
            return incident
        
        if metrics["db_connections"]>DB_CONN_THRESHOLD:
            incident=Incident(
                incident_type="DBB_CONN_EXHAUSTION",
                metrics_snapshot=metrics
            )
            incident.log_event("DB connection exhaustion detected")
            return incident
        
        return None