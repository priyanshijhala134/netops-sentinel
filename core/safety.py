import time

COOLDOWN = 60
_last_action = 0

def can_act():
    global _last_action
    now = time.time()
    if now - _last_action < COOLDOWN:
        return False
    _last_action = now
    return True
