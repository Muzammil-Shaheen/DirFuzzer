#!/usr/bin/env python3

import requests
import argparse
import concurrent.futures
from queue import Queue
from colorama import Fore, init
from tqdm import tqdm
from pyfiglet import Figlet

init(autoreset=True)

# Create the "DRF" ASCII banner
f = Figlet(font='big')
banner_lines = f.renderText("DRFZ").splitlines()

# Info lines below the banner
info_lines = [
    "DirFuzzer by Shaheen",
    "Fast & Accurate Directory Fuzzer | v1.0"
]

# Calculate max width for border
max_width = max(
    max(len(line) for line in banner_lines),
    max(len(line) for line in info_lines)
) + 4  # padding

# Top border
print(Fore.RED + "\033[1m" + "╔" + "═" * max_width + "╗")

# Banner lines
for line in banner_lines:
    print("║ " + line.ljust(max_width - 2) + " ║")

# Separator line
print("╟" + "─" * max_width + "╢")

# Info lines
for line in info_lines:
    print("║ " + line.center(max_width - 2) + " ║")

# Bottom border
print("╚" + "═" * max_width + "╝" + "\033[0m\n")

# Argument Parsing
parser = argparse.ArgumentParser(description="Blazing Fast Directory Fuzzer")
parser.add_argument("-u", "--url", required=True, help="Target URL (e.g. https://example.com/)")
parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
parser.add_argument("-t", "--threads", type=int, default=50, help="Number of concurrent threads")
parser.add_argument("-s", "--status", type=int, nargs="+", default=[200, 301, 302, 403], help="Show only these status codes")
parser.add_argument("--timeout", type=int, default=4, help="Request timeout (sec)")
parser.add_argument("--ua", default="DirFuzzer/3.0", help="User-Agent")
parser.add_argument("-x", "--extensions", default=".php,.html", help="Comma-separated extensions")
parser.add_argument("--limit", type=int, help="Limit number of words to load from wordlist")
parser.add_argument("--delay", type=float, default=0.0, help="Delay between requests (seconds)")

args = parser.parse_args()
args.extensions = args.extensions.split(",")
headers = {"User-Agent": args.ua}

# Load wordlist
with open(args.wordlist, "r") as f:
    words = [line.strip() for line in f if line.strip()]
    if args.limit:
        words = words[:args.limit]

# Build URL queue
url_queue = Queue()
for word in words:
    for ext in args.extensions:
        full_url = args.url.rstrip("/") + f"/{word}{ext}"
        url_queue.put(full_url)

progress = tqdm(total=url_queue.qsize(), desc="Fuzzing", ncols=80)

# Request function
def fetch_url(url):
    try:
        r = requests.get(url, headers=headers, timeout=args.timeout, allow_redirects=False)
        if r.status_code in args.status:
            color = (
                Fore.GREEN if r.status_code == 200 else
                Fore.YELLOW if r.status_code in [301, 302] else
                Fore.RED
            )
            print(f"{color}[{r.status_code}] {url}")
    except requests.RequestException:
        pass
    finally:
        progress.update(1)

# Threaded Execution
with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
    while not url_queue.empty():
        url = url_queue.get()
        executor.submit(fetch_url, url)
        if args.delay:
            import time
            time.sleep(args.delay)

progress.close()
