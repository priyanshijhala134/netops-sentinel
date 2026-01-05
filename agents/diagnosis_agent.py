class DiagnosisAgent:
    def diagnosis(self,incident):
        # LLM REASONING
        if incident.incident_type=="HIGH LATENCY":
            diagnosis={
                "root_cause":"DB_CONN_EXHAUSTION",
                "confidence":0.81,
                "reasoning":"Latency without CPU spikes indicates downstream bottleneck"
            }
        else:
            diagnosis={
                "root_cause":incident.incident_type,
                "confidence":0.9,
                "reasoning":"Direct metric correlation"
            }      
        incident.diagnosis=diagnosis
        incident.status="DIAGNOSED"
        incident.log_event(f"Diagnosed as {diagnosis['root_cause']}")
        return incident