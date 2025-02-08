import paramiko
import threading

servers = [
    {"ip": "192.168.82.222", "user": "dhpcsa", "start": 0, "end": 200, "password": "dhpcsa"},
    {"ip": "192.168.82.218", "user": "dhpcsa", "start": 201, "end": 399, "password": "dhpcsa"},
    {"ip": "192.168.82.17", "user": "dhpcsa", "start": 400, "end": 494, "password": "dhpcsa"},
]

script_path = "/home/dhpcsa/fetch_weather.py"

def run_remote_script(server):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote server
        ssh.connect(server["ip"], username=server["user"], password=server["password"])
        
        command = f"python3 {script_path} {server['start']} {server['end']}"
        stdin, stdout, stderr = ssh.exec_command(command)

        print(f"Output from {server['ip']}:\n", stdout.read().decode())
        print(f"Errors from {server['ip']}:\n", stderr.read().decode())

        ssh.close()
    except Exception as e:
        print(f"Error running script on {server['ip']}: {e}")

# List to store all threads
threads = []

# Start threads for each server
for server in servers:
    thread = threading.Thread(target=run_remote_script, args=(server,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All scripts executed in parallel!")
