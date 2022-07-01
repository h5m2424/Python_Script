"""
# mail example

[Server]: Server_1
[Time]: 2020/06/22-20:48:01
[CPU_Used]: 16 %
[MEM_Available]: 3562 MB (44 %)
"""

import time
import psutil
import yagmail
import socket

e_from = "xxx@qq.com"
e_password = "xxxxxx"
e_host = "smtp.qiye.aliyun.com"
e_to = ['xxx@qq.com','xxx@hotmail.com']
e_cc = "xxx@qq.com"
#e_bcc = ""
e_subject = "cpu & 内存使用率警告"
e_attachments = []
cpu_warning_point = 80   # 单位：%（大于此值发送警告）
mem_warning_point = 10  # 单位：%（小于此值发送警告）
check_time = 60    # 单位：秒（检测间隔）
hostname = socket.gethostname()

def send(time_formated, detials):
    
    #创建yagmail.SMTP实例
    yag = yagmail.SMTP(user = e_from, password = e_password, host = e_host) #SMTP服务器域名

    yag.send(to = e_to,
         cc = e_cc, #抄送
         #bcc = e_bcc, #密送
         subject = hostname + " | " + e_subject,
         contents = "[Server]: " + hostname + "\n[Time]: " + time_formated + "\n[CPU_Used]: " + detials[0] + "\n[MEM_Available]: " + detials[1],
         attachments = e_attachments)
 
while True:
    time.sleep(check_time)
    time_formated = time.strftime("%Y/%m/%d-%H:%M:%S")
    cpu_percent = int(psutil.cpu_percent())
    avalb_mem = int(int(psutil.virtual_memory().available) / 1024 / 1024)    # 单位换算成 MB
    mem_percent = int(psutil.virtual_memory().percent)
    detials = (str(cpu_percent) + " %", str(avalb_mem) + " MB" + " (" + str(100 - mem_percent) + " %" + ")")
 
    if cpu_percent >= cpu_warning_point or (100 - mem_percent) <= mem_warning_point:
        send(time_formated, detials)
        print("Warning mail sent: " + "\n[Time]: " + time_formated + "\n[CPU_Used]: " + detials[0] + "\n[MEM_Available]: " + detials[1] + "\n")
    else:
        print("passed: " + "\n[Time]: " + time_formated + "\n[CPU_Used]: " + detials[0] + "\n[MEM_Available]: " + detials[1] + "\n")
