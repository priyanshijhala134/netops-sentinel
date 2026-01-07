from agents.tools import restart_service

def heal(state:str):
    if state=="HIGH_CPU":
        print("High CPU detected.Restarting nginx...")
        success=restart_service("nginx")
        return success
    return False