import smtplib
import time
import psutil
import logging;logging.basicConfig(level=logging.INFO)
from email.mime.text import MIMEText
 
def send(time_formated, detials):
    msg = MIMEText(time_formated + "\n[CPU_Used]: " + detials[0] + "\n[MEM_Available]: " + detials[1])
    logging.debug(msg.as_string())
    msg["Subject"] = subject
    msg["From"] = e_from
    msg["To"] = e_to

    server = smtplib.SMTP(host, port)
    try:
        server.login(e_from, password)
        server.sendmail(e_from, e_to, msg.as_string())
        logging.info("send success" + "\n")
    except Exception as e:
        logging.error("send fail", e + "\n")
    finally:
        server.quit()
 
e_from = "*****@aliyun.com"
password = "******"
e_to = "*****@qq.com"
host = "smtp.qiye.aliyun.com"
port = 25
subject = "cpu & 内存使用率警告"
cpu_warning_point = 65   # 单位：%（大于此值发送警告）
mem_warning_point = 20  # 单位：%（小于此值发送警告）
check_time = 5    # 单位：秒（检测间隔）
 
while True:
    time.sleep(check_time)
    time_formated = time.strftime("%Y/%m/%d-%H:%M:%S")
    cpu_percent = int(psutil.cpu_percent())
    avalb_mem = int(psutil.virtual_memory().available) / 1024 / 1024    # 单位换算成 MB
    mem_percent = int(psutil.virtual_memory().percent)
    detials = (str(cpu_percent) + " %", str(avalb_mem) + " MB" + " (" + str(100 - mem_percent) + " %" + ")")
    logging.info(time_formated)
    logging.info("[CPU_Used]: " + detials[0])
    logging.info("[MEM_Available]: " + detials[1])
 
    if cpu_percent >= cpu_warning_point or (100 - mem_percent) <= mem_warning_point:
        send(time_formated, detials)
    else:
        print("passed" + "\n")
