from dataclasses import dataclass,field
from typing import Dict,List
from datetime import datetime
import uuid #universally unique indentifier

@dataclass
class Incident:
    id:str=field(default_factory=lambda:str(uuid.uuid4()))
    status:str="DETECTED"
    incident_type:str=""
    metrics_snapshot:Dict=field(default_factory=dict)
    diagnosis:Dict=field(default_factory=dict)
    action_taken:Dict=field(default_factory=dict)
    timeline:List[Dict]=field(default_factory=list)

    def log_event(self,message:str):
        self.timeline.append({
            "timestamp":datetime.timezone.isoformat(),
            "message":message
        })
        