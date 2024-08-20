import pathlib
import logging
import time
import json
import os
import argparse

# Configure logging
logging.basicConfig(filename='scan.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Command-line arguments
parser = argparse.ArgumentParser(description='Scan configuration')
parser.add_argument('--threads', type=int, default=1024, help='Number of threads')
parser.add_argument('--timeout', type=int, default=3, help='Timeout in seconds')
parser.add_argument('--proxy', type=str, default=None, help='Proxy address (e.g., http://127.0.0.1:8080)')
parser.add_argument('--user-agent', type=str, default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', help='User-Agent header')
parser.add_argument('--rate-limit', type=int, default=10, help='Number of requests per second')
parser.add_argument('--retry', type=int, default=3, help='Number of retries for failed requests')
args = parser.parse_args()

# Port configurations
default_ports = {80}  # Default ports
small_ports = {80, 443, 8000, 8080, 8443}
medium_ports = {80, 81, 443, 591, 2082, 2087, 2095, 2096, 3000, 8000, 8001,
                8008, 8080, 8083, 8443, 8834, 8888}
large_ports = {80, 81, 300, 443, 591, 593, 832, 888, 981, 1010, 1311, 2082,
               2087, 2095, 2096, 2480, 3000, 3128, 3333, 4243, 4567, 4711,
               4712, 4993, 5000, 5104, 5108, 5800, 6543, 7000, 7396, 7474,
               8000, 8001, 8008, 8014, 8042, 8069, 8080, 8081, 8088, 8090,
               8091, 8016, 8118, 8123, 8172, 8222, 8243, 8280, 8281, 8333,
               8443, 8500, 8834, 8880, 8888, 8983, 9000, 9043, 9060, 9080,
               9090, 9091, 9200, 9443, 9800, 9981, 12443, 16080, 18091, 18092,
               20720, 28017}  # Add more ports if needed
ports = {'default': default_ports, 'small': small_ports,
         'medium': medium_ports, 'large': large_ports}

# Configuration settings
ignore_status_code = [400]
verify_ssl = False
allow_redirects = True
threads = args.threads
timeout = args.timeout
rate_limit = args.rate_limit
retry = args.retry
proxy = args.proxy
user_agent = args.user_agent

# Function to make a request with retry logic
def make_request_with_retries(url, retries=retry):
    for attempt in range(retries):
        try:
            # Make request here, considering proxy, user_agent, etc.
            # Placeholder for request code
            break
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f'Failed to make request to {url}: {e}')

# Result save path
realpath = pathlib.Path(__file__).parent
result_save_path = realpath.joinpath('results')

# Print the updated settings
print(f"Ports configuration: {ports}")
print(f"Ignore status codes: {ignore_status_code}")
print(f"SSL verification: {verify_ssl}")
print(f"Allow redirects: {allow_redirects}")
print(f"Number of threads: {threads}")
print(f"Timeout: {timeout}")
print(f"Rate limit: {rate_limit} requests per second")
print(f"Number of retries: {retry}")
print(f"Proxy address: {proxy}")
print(f"User-Agent: {user_agent}")
print(f"Results will be saved to: {result_save_path}")

# Example function to save results as JSON
def save_results_as_json(results, file_path):
    with open(file_path, 'w') as f:
        json.dump(results, f, indent=4)
