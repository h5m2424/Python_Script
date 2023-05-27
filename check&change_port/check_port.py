import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# 定义服务器和用户名
server = "world.hello.com"
router = "192.168.10.254"
user_server = "root"
user_router = "admin"

# 读取存储端口号的文件
with open('port.txt', 'r') as f:
    port = int(f.read().strip())

# 检查服务器的端口是否通
result = os.system(f'nc -z -w 3 {server} {port}')
if result != 0:
    result = 'Port was blocked!'
    # 远程连接服务器执行命令
    ssh_server = subprocess.Popen(['ssh', f'{user_server}@{server}', f'sed -i "2,3s/{port}/{port+1}/" /etc/nginx/sites-available/default && systemctl restart nginx.service'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_server, error_server = ssh_server.communicate()
    if output_server is None:
        output_server = b''
    if error_server is None:
        error_server = b''
    # 远程连接路由器执行命令
    ssh_router = subprocess.Popen(['ssh', f'{user_router}@{router}', f'sed -i "336s/{port}/{port+1}/;349s/{port}/{port+1}/;366s/{port}/{port+1}/;1320s/{port}/{port+1}/" /koolshare/ss/ssconfig.sh && sh /koolshare/ss/ssconfig.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_router, error_router = ssh_router.communicate()
    if output_router is None:
        output_router = b''
    if error_router is None:
        error_router = b''
    # 发送邮件通知
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = MIMEText(f'端口 {port} 不可用！新的端口：{port+1}.')
    msg['Subject'] = f'{timestamp} - VPN端口修改通知'
    msg['From'] = 'warning@hello.com'
    msg['To'] = 'postmaster@hello.com'
    smtp = smtplib.SMTP('smtp.qiye.aliyun.com')
    smtp.login('warning@hello.com', '********')
    smtp.sendmail('warning@hello.com', 'postmaster@hello.com', msg.as_string())
    smtp.quit()
    # 更新存储端口号的文件
    with open('port.txt', 'w') as f:
        f.write(str(port+1))
    # 写入日志文件
    with open('log.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - Port {port} check result: {result}\n')
        f.write(f'{timestamp} - Server command output: {output_server.decode()}\n')
        f.write(f'{timestamp} - Server command error: {error_server.decode()}\n')
        f.write(f'{timestamp} - Router command output: {output_router.decode()}\n')
        f.write(f'{timestamp} - Router command error: {error_router.decode()}\n')
else:
    result = 'Port is open.'
    output_server = b''
    error_server = b''
    output_router = b''
    error_router = b''
    # 写入日志文件
    with open('log.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} - Port {port} check result: {result}\n')
