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
