import os
import requests
import platform
import subprocess
from datetime import datetime

class AdBlocker:
    def __init__(self):
        # Define hosts file location based on OS
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if platform.system() == "Windows" else "/etc/hosts"
        self.ad_domains_url = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
        
    def backup_hosts(self):
        # Create backup of original hosts file
        backup_path = self.hosts_path + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(self.hosts_path, 'r') as original, open(backup_path, 'w') as backup:
            backup.write(original.read())
        print(f"Backup created at {backup_path}")

    def update_hosts(self):
        try:
            # Download ad domains list
            response = requests.get(self.ad_domains_url)
            ad_domains = response.text
            
            # Backup existing hosts file
            self.backup_hosts()
            
            # Update hosts file
            with open(self.hosts_path, 'w') as hosts_file:
                hosts_file.write(ad_domains)
            
            # Flush DNS cache
            if platform.system() == "Windows":
                subprocess.run(["ipconfig", "/flushdns"], check=True)
            else:
                subprocess.run(["sudo", "systemctl", "restart", "systemd-resolved"], check=True)
                
            print("Ad blocking rules updated successfully!")
            
        except Exception as e:
            print(f"Error updating hosts file: {str(e)}")

    def restore_backup(self, backup_path):
        try:
            with open(backup_path, 'r') as backup, open(self.hosts_path, 'w') as hosts:
                hosts.write(backup.read())
            print("Hosts file restored from backup!")
        except Exception as e:
            print(f"Error restoring backup: {str(e)}")

if __name__ == "__main__":
    # Note: Run this script with admin/root privileges
    blocker = AdBlocker()
    blocker.update_hosts()