import re, ipaddress
# Path to the log file
logFilePath = "./nodejsapp.log"
counterDict = {}

# ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

ipv4_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|\b(?:[0-9a-fA-F]{1,4}:)::[0-9a-fA-F]{0,4}(?::[0-9a-fA-F]{1,4})\b'
ip_pattern = f'({ipv4_pattern}|{ipv6_pattern})'

with open(logFilePath) as f:
    for line in f:
        try:
            userIP = line.split(" ")[1]
            if re.search(ip_pattern, userIP):
                # ipaddress.ip_address(userIP)
                counterDict[userIP] = counterDict.get(userIP, 0) + 1
            else:
                continue
        except IndexError:
            pass

# Print the number of unique IP addresses and the addresses themselves
print("Unique IP Count:", len(counterDict))

for ip, count in counterDict.items():
    print(f"IP: {ip}: Count: {count}")

