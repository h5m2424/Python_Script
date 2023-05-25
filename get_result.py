""" 
coding : utf-8

脚本说明：
本脚本作用为批量远程登录到Linux主机并执行特定的命令，把返回的结果存到文件里
需要把“主机ip“，”SSH端口号“，”SSH用户名"，“SSH密码”按照顺序
提前写到“host_list.txt”文件(host_list.txt文件和get_result.py脚本放同目录)，每一行写一个主机，用引号包住每个字段，用逗号隔开。
例：
'10.0.0.1','22','username','password'
'10.0.0.2','22','username','password'
执行方法：
python3 get_result.py
"""
import paramiko

# 获取需要执行的命令
command = input("请输入需要在批量主机上执行的命令：")
# 创建ssh对象(客户端）
ssh = paramiko.SSHClient()
# 自动添加新主机密钥
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 打开主机列表，逐个连接并执行命令获取结果
with open ("host_list.txt", "r") as f:
    while True:
        line = f.readline()
        # 遇到空行关闭循环
        if not line:
            break
        host_tuple = eval(line)
        host = list()
        host.append(host_tuple)
        for HostName,Port,UserName,PassWord in host:
            # 发起远程连接
            ssh.connect(HostName,Port,UserName,PassWord)
            # 在远程执行linux命令，用字符串的形式传递命令,exec_command会返回三个参数
            stdin,stdout,stderr = ssh.exec_command(command)
            # 打印执行结果，读取出来的stdout内容可以用read读取
            result=stdout.read().decode("utf8")
            print(result)
            # 结果写入文件
            with open("result.txt", "a") as f2:
                f2.writelines(HostName)
                f2.write("\n")
                f2.writelines(result)
                f2.writelines("--------------------")
                f2.write("\n\n")
            ssh.close()
        # 新起一行继续
        line = line.rstrip("\n")
