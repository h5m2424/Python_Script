import sys
import os
import time
import yagmail

port_file = "/root/check_port/port.txt"
log_file = "/root/check_port/log.txt"
nginx_conf = "/etc/nginx/sites-available/default"
check_port = int(open(port_file).readline()[:-1])
new_check_port = check_port + 1
now = int(time.time())
time_struct = time.localtime(now)
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
e_from = "xxx@****.com"
e_password = "****"
e_host = "smtp.****.com"
e_to = "xxx@****.com"
e_cc = []
#e_bcc = ""
e_attachments = []

# 发送端口被封邮件函数
def send_mail():
    #创建yagmail.SMTP实例
    yag = yagmail.SMTP(
        user = e_from,
        password = e_password,
        host = e_host
        )
    yag.send(
        to = e_to,
        cc = e_cc, #抄送
        #bcc = e_bcc, #密送
        subject = "Port" + " " + str(check_port) + " " + "was blocked",
        contents = "Port" + " " + str(check_port) + " " + "was blocked" + " " + "\n" + " " + "Port was changed to" + " " + str(new_check_port),
        attachments = e_attachments
        )
    print("Alert mail sent to administrator")

# 修改端口函数
def change_port():
    search_text = str(check_port)
    replace_text = str(new_check_port)
    with open(port_file, "w", encoding="utf-8") as fo:
        fo.write(str(new_check_port) + "\n")
    print("Port was changed to", new_check_port)    
    with open(nginx_conf, 'r', encoding='UTF-8') as file:
        data = file.read()
        data = data.replace(search_text, replace_text, 2)
    with open(nginx_conf, 'w', encoding='UTF-8') as file:
        file.write(data)
    restart_nginx = os.system('systemctl restart nginx.service')
    if restart_nginx == 0:
        print("Nginx port was change to", new_check_port)
        print("Waiting for next checking...")
    else:
        print("Nginx failed to restart")

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
    print(time_str, ":", "Port", check_port, "was blocked!")
    send_mail()
    change_port()
