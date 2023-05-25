import socket
import sys
import os
import time
import paramiko

ip_file = "/root/check_port/ip.txt"
port_file = "/root/check_port/port.txt"
log_file = "/root/check_port/log.txt"
check_ip = open(ip_file).readline()[:-1]
check_port = int(open(port_file).readline()[:-1])
new_check_port = check_port + 1
check_timeout = 30
command = "python3 /root/check_port/change_port.py"
hostname = "x.x.x.x"
user = "root"
pkey='/root/.ssh/id_rsa'
now = int(time.time())
time_struct = time.localtime(now)
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)

# 检测端口函数
def check():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(check_timeout)
    result = sock.connect_ex((check_ip, check_port))
    if result == 0:
        print("Port", check_port, "is open")
        sock.close
    else:
        print("Port", check_port, "was blocked! Start connect to remote server for continuing...")
        with open(port_file, "w", encoding="utf-8") as fo:
            fo.write(str(new_check_port) + "\n")
        print("Port was changed to", new_check_port) 
        key=paramiko.RSAKey.from_private_key_file(pkey)
        paramiko.util.log_to_file('paramiko.log')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username = user, pkey = key)
        stdin,stdout,stderr=ssh.exec_command(command)
        print(stdout.readlines())  

# 日志模块
class Logger(object):
    def __init__(self, filename=log_file):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
sys.stdout = Logger(log_file)
print(os.path.dirname(__file__))

if __name__ == '__main__':
    print(time_str, ":", "Checking port...")
    check()
