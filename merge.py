import subprocess
import pandas as pd

# Define worker nodes and their report file paths
nodes = ["192.168.82.222", "192.168.82.218", "192.168.82.17"]
remote_file_path = "/home/dhpcsa/final_report.csv"  # Update this path as needed
local_file_path = "final_weather_report.csv"

# Initialize final DataFrame
final_df = pd.DataFrame()

# Loop through all nodes and fetch their reports
for node in nodes:
    print(f"Fetching report from {node}...")
    subprocess.run(["scp", f"dhpcsa@{node}:{remote_file_path}", f"weather_report_{node}.csv"])

    # Read the downloaded CSV file
    df = pd.read_csv(f"weather_report_{node}.csv")
    final_df = pd.concat([final_df, df], ignore_index=True)

# Save the final merged report
final_df.to_csv(local_file_path, index=False)
print(f"✅ Final merged report saved as {local_file_path}")
