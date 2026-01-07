import requests

PROMETHEUS_URL="http://localhost:9090/api/v1/query"


def get_avg_cpu():
    data = query_prometheus('rate(container_cpu_usage_seconds_total{name="nginx"}[30s])')
    values = [
        float(item["value"][1])
        for item in data["data"]["result"]
    ]
    avg_cpu = sum(values) / len(values)
    print("DEBUG: avg_cpu=", avg_cpu)
    
    return avg_cpu

def query_prometheus(query:str):
    response=requests.get(
        PROMETHEUS_URL,
        params={"query":query}
    )
    return response.json()

if __name__=="__main__":
    print("CPU: ", get_avg_cpu())
# FAKE METRICS 
# from core.incident import Incident
# # monitoring logic
# CPU_THRESHOLD=85
# LATENCY_THRESHOLD=300
# DB_CONN_THRESHOLD=90

# class MonitoringAgent:
#     def defect(self,metrics:dict)->Incident|None:
#         if metrics["cpu"]>CPU_THRESHOLD:
#             incident=Incident(
#                 incident_type="HIGH_CPU",
#                 metrics_snapshot=metrics
#             )
#             incident.log_event("High cpu detected")
#             return incident
        
#         if metrics["latency"]>LATENCY_THRESHOLD:
#             incident=Incident(
#                 incident_type="HIGH_LATENCY",
#                 metrics_snapshot=metrics
#             )
#             incident.log_event("High latency detected")
#             return incident
        
#         if metrics["db_connections"]>DB_CONN_THRESHOLD:
#             incident=Incident(
#                 incident_type="DBB_CONN_EXHAUSTION",
#                 metrics_snapshot=metrics
#             )
#             incident.log_event("DB connection exhaustion detected")
#             return incident
        
#         return None