# flow controller
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) # gets 'core'
parent_dir = os.path.dirname(current_dir)                # gets 'netops-sentinel'

sys.path.append(parent_dir)

from agents.monitoring_agent import get_avg_cpu
from agents.healing_agent import heal
import time

def monitor_state():
    print("agent started")
    cpu=get_avg_cpu()
    
    if cpu>0.3:
        state = "HIGH_CPU"
    else:
        state = "NORMAL"
    print("Current State: ",state)
    
    if state!="NORMAL":
        healed=heal(state)
        time.sleep(5) #system to stabilise
        cpu_after=get_avg_cpu()
        print("CPU after healing: ", cpu_after)
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