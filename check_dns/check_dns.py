import dns.resolver
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# 域名列表文件路径
domain_list_file = "domain_list.txt"
# 收件人列表文件路径
receiver_list_file = "receiver_list.txt"
# 日志文件路径
log_file = "dns_log.txt"

# SMTP服务器配置
smtp_server = "smtp.****.com"
smtp_port = 25
smtp_username = "****@****.com"
smtp_password = "********"
sender_email = "****@****.com"

# 读取域名列表
with open(domain_list_file, "r") as file:
    domains = file.read().splitlines()

# 读取收件人列表
with open(receiver_list_file, "r") as file:
    receiver_emails = file.read().splitlines()

# 解析域名并发送邮件告警
with open(log_file, "a") as log:
    for domain in domains:
        try:
            answers = dns.resolver.resolve(domain, "A")
            ip_addresses = [str(rdata) for rdata in answers]
            log_message = f"[{datetime.now()}] Domain: {domain}, IP Addresses: {', '.join(ip_addresses)}"
            log.write(log_message + "\n")

        except dns.resolver.NXDOMAIN:
            log_message = f"[{datetime.now()}] Domain: {domain}, Error: NXDOMAIN"
            log.write(log_message + "\n")

            # 发送邮件告警
            subject = f"域名解析失败！: {domain}"
            message = f"域名 {domain} 无法解析 (NXDOMAIN error)."
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = ", ".join(receiver_emails)

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    server.sendmail(sender_email, receiver_emails, msg.as_string())
                log_message = f"[{datetime.now()}] Email notification sent successfully for domain: {domain}"
                log.write(log_message + "\n")

            except Exception as e:
                log_message = f"[{datetime.now()}] Failed to send email notification for domain: {domain}: {e}"
                log.write(log_message + "\n")
