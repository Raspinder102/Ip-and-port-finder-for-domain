import socket
from urllib.parse import urlparse

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_ip_address(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def tcp_connect_scan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            return "Open"
        else:
            return "Closed"
    except socket.error:
        return "Error"
    finally:
        sock.close()

def main():
    url = input("Enter target URL or domain: ")
    port = input("Enter port number (default is 80): ") or "80"
    
    try:
        port = int(port)
    except ValueError:
        print("Port must be a number")
        return

    domain = extract_domain(url) if "://" in url else url
    if not domain:
        print("Invalid URL or domain")
        return

    ip = get_ip_address(domain)
    if ip:
        print(f"Resolved {domain} to IP: {ip}")
    else:
        print(f"Could not resolve {domain}")
        return

    print(f"Scanning {ip} (from {domain}) on port {port}")
    result = tcp_connect_scan(ip, port)
    print(f"Port {port} is {result}")

if __name__ == "__main__":
    main()
