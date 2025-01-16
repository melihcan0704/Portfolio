#Quick script to constantly ping a remote server to see if its available and quickly deploy your files to the remote directory using rsync from kernel.

import subprocess
import time

def ping(host):
    """Ping the remote host to check if it's reachable."""
    try:
        # Send one ping (-c 1) and wait for 1 second (-W 1) for a reply.
        output = subprocess.run(['ping', '-c', '1', '-W', '1', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output.returncode == 0
    except Exception as e:
        print(f"Error pinging host: {e}")
        return False

def run_rsync():
    """Run the rsync command."""
    try:
        # rsync command with specified options
        rsync_command = [
            'rsync', '--partial', '--progress', '-e', 'ssh -p 22', 
            '/home/user/yourdirectory', 'user@remote_ip_address:/home/remote_directory'
        ]
        subprocess.run(rsync_command)
        print("Rsync completed successfully.")
    except Exception as e:
        print(f"Error running rsync: {e}")

def monitor_host_and_sync(host):
    """Monitor the host, run rsync when the host is available."""
    host_available = False

    while True:
        if ping(host):
            if not host_available:
                print(f"Host {host} is now available.")
                host_available = True
            run_rsync()
        else:
            if host_available:
                print(f"Host {host} is now unavailable.")
                host_available = False

        time.sleep(5)  # Wait for 5 seconds before the next check

if __name__ == "__main__":
    remote_host = "remote_ip_address"

    monitor_host_and_sync(remote_host)
