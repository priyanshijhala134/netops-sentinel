
class ActionAgent:
    def act(self,incident):
        if incident.diagnosis["confidence"]<0.75:
            incident.status="ESCALATED"
            incident.log_event("Confidence too low,escalating")
            return incident
        
        root=incident.diagnosis["root_cause"]
        
        if root=="DB_CONN_EXHAUSTION":
            action=="restart_postgres"
        elif root=="HIGH_CPU":
            action=="restart_app"
        else:
            action="clear_cache"
        
        incident.action_taken = {
            "action":action
        }
        incident.status="FIX_APPLIED"
        incident.log_event(f"Action executed: {action}")
        return incident
        