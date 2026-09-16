import subprocess
import time
import os

# Kill any existing ssh processes that might be running pinggy
os.system("taskkill /f /im ssh.exe")

print("Starting tunnel...")
# Run SSH in the background
# We use -t to force a pseudo-terminal which pinggy needs to show the URL
# We use -o StrictHostKeyChecking=no to skip the yes/no prompt
process = subprocess.Popen(
    ["ssh", "-t", "-o", "StrictHostKeyChecking=no", "-o", "ExitOnForwardFailure=yes", "-p", "443", "-R0:localhost:5000", "a.pinggy.io"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    shell=True # Use shell for Windows to handle ssh better
)

# Path to save the URL
url_file = "tunnel_url.txt"

# Search for the URL in the output
with open(url_file, "w") as f:
    f.write("Starting...\n")

found_url = False
start_time = time.time()
while time.time() - start_time < 30: # Wait up to 30 seconds
    line = process.stdout.readline()
    if line:
        with open(url_file, "a") as f:
            f.write(line)
        if ".pinggy.link" in line or ".pinggy.io" in line:
            print(f"Found URL: {line.strip()}")
            found_url = True
            break
    time.sleep(0.1)

if not found_url:
    print("Could not find URL in time. Check tunnel_url.txt")
