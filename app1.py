from datetime import datetime, timedelta
import re
from collections import defaultdict, Counter

with open("./nodejsapp.log", 'r') as file:
    log_data = file.readlines()
 

# Regex pattern to parse the log
log_pattern = re.compile(
    r'(?P<timestamp>[\d\-T:\.Z]+)\s(?P<ip>[\d\.]+).*?"(?P<method>\w+)\s(?P<endpoint>\/[^\s]*)\sHTTP\/[\d\.]+"\s\d+\s-\s".*?"\s"(?P<user_agent>.*?)"'
)

# Parsed log list
parsed_logs = []

for line in log_data:
    match = log_pattern.match(line)
    if match:
        ts = datetime.strptime(match.group("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
        parsed_logs.append({
            "timestamp": ts,
            "ip": match.group("ip"),
            "endpoint": match.group("endpoint"),
            "user_agent": match.group("user_agent"),
        })

# --- Task 1: Requests per IP in 10 sec window after first request ---
ip_times = defaultdict(list)
for log in parsed_logs:
    ip_times[log["ip"]].append(log["timestamp"])

ip_request_counts = {}
for ip, times in ip_times.items():
    times.sort()
    first_time = times[0]
    window_end = first_time + timedelta(seconds=10)
    count = sum(1 for t in times if first_time < t <= window_end)
    ip_request_counts[ip] = count

# --- Task 2: Count requests per user agent ---
user_agent_counter = Counter(log["user_agent"] for log in parsed_logs)

# --- Task 3: Count accesses per endpoint ---
endpoint_counter = Counter(log["endpoint"] for log in parsed_logs)

# --- Output Results ---
print("Requests within 10 seconds of the first request per IP:")
for ip, count in ip_request_counts.items():
    print(f"{ip}: {count} requests")

print("\nRequest count by User Agent:")
for agent, count in user_agent_counter.items():
    print(f"{agent}: {count} requests")

print("\nEndpoint access counts:")
for endpoint, count in endpoint_counter.items():
    print(f"{endpoint}: {count} accesses")
