# flow controller
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)                

sys.path.append(parent_dir)

from agents.monitoring_agent import get_avg_cpu
from agents.healing_agent import heal
from core.reporter import generate_incident_report, save_report

def monitor_state():
    print("agent started")
    
    # FIX 1: Get the CPU value once and use it
    time.sleep(30)
    cpu = get_avg_cpu()
    cpu_before = cpu 
    
    if cpu > 0.3:
        state = "HIGH_CPU"
    else:
        state = "NORMAL"
        
    print("Current State: ", state)
    
    # FIX 2: Only generate report if state is NOT normal
    if state != "NORMAL":
        healed = heal(state)
        time.sleep(5) # system to stabilise
        
        cpu_after = get_avg_cpu() # This defines cpu_after
        print("CPU after healing: ", cpu_after)
        
        # Only create report if we actually did something
        report = generate_incident_report(
            incident_type="HIGH_CPU",
            cpu_before=cpu_before,
            cpu_after=cpu_after,  # Now safe to use
            action_taken="restart_nginx",
            success=cpu_after < cpu_before
        )

        save_report(report)
        print("Incident report saved")
    else:
        print("System is healthy. No report needed.")

if __name__=="__main__":
    monitor_state()
        
# FAKE METRICS
# from agents.monitoring_agent import MonitoringAgent
# from agents.monitoring_agent import MonitoringAgent
# from agents.diagnosis_agent import DiagnosisAgent
# from agents.audit_agent import AuditAgent
# from agents.action_agent import ActionAgent

# class NetOpsStateMachine:
#     def __init__(self):
#         self.monitor=MonitoringAgent()
#         self.diagnose=DiagnosisAgent()
#         self.act=ActionAgent()
#         self.audit=AuditAgent()
        
        
#     def run(self,metrics,post_action_metrics):
#         incident=self.monitor.detect(metrics)
#         if not incident:
#             return None
#         incident=self.diagnose.diagnose(incident)
#         incident=self.act.act(incident)
#         incident=self.audit.audit(incident)
        
#         return incident