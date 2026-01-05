# verification
class AuditAgent:
    def verify(self,incident,new_metrics):
        improved= (
            new_metrics["cpu"]< incident.metrics_snapshot["cpu"] and
            new_metrics["latency"]<incident.metrics_snapshot["latency"])
        
        if improved:
            incident.statis="RESOLVED"
            incident.log_event("Incident resolved successfully")
        else:
            incident.status="FAILED"
            incident.log_event("Fix failed, rollback needed")
        return incident