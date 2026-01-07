import subprocess

def restart_service(service_name: str)->bool:
    """
    restarts docker + returns true if successful
    """
    try:
        subprocess.run(
            ["docker","restart",service_name],
            check=True,
            stdout= subprocess.PIPE,
            stderr= subprocess.PIPE   
        )
        return True
    except subprocess.CalledProcessError as e:
        print("restart failed: ",e)
        return False