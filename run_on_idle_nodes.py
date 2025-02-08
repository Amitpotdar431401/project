import subprocess
import requests

PROMETHEUS_URL = "http://192.168.82.222:9090/api/v1/query"
script_path = "/home/dhpcsa/fetch_weather.py"

# Define nodes with workload distribution
nodes = [
    {"ip": "192.168.82.222", "start": 0, "end": 200},
    {"ip": "192.168.82.218", "start": 201, "end": 399},
    {"ip": "192.168.82.17", "start": 400, "end": 494},
]

idle_nodes = []

# Function to fetch CPU usage
def get_cpu_usage(node_ip):
    query = f'100 - (avg by(instance) (rate(node_cpu_seconds_total{{instance="{node_ip}:9100", mode="idle"}}[30s])) * 100)'
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    result = response.json()

    if result["status"] == "success" and result["data"]["result"]:
        return float(result["data"]["result"][0]["value"][1])
    return None

# 1️⃣ Check CPU usage & find idle nodes
for node in nodes:
    cpu_usage = get_cpu_usage(node["ip"])
    if cpu_usage is not None:
        print(f"Node {node['ip']} CPU Usage: {cpu_usage:.2f}%")
        if cpu_usage < 20:  # Consider node idle if CPU usage < 20%
            idle_nodes.append(node)

print("\n✅ Idle Nodes:", [node["ip"] for node in idle_nodes])

# 2️⃣ Run fetch_weather.py in parallel on idle nodes with arguments
processes = []
for node in idle_nodes:
    print(f"🚀 Running fetch_weather.py on {node['ip']} with range {node['start']} to {node['end']}...")
    process = subprocess.Popen([
        "ssh", f"dhpcsa@{node['ip']}", f"python3 {script_path} {node['start']} {node['end']}"
    ])
    processes.append(process)

# 3️⃣ Wait for all processes to complete
for process in processes:
    process.wait()

print("\n✅ All scripts executed in parallel on idle nodes!")
