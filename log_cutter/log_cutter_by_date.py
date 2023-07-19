import os
import datetime
import shutil

def split_log_by_date(log_path, output_path):
    # 获取当前日期
    current_date = datetime.datetime.now().date()

    # 切割日期
    split_date = current_date.strftime("%Y-%m-%d")

    # 切割后的文件名
    file_name = os.path.basename(log_path)
    new_file_name = os.path.join(output_path, f"{split_date}_{file_name}")

    # 切割日志文件
    shutil.copy2(log_path, new_file_name)

    # 清空原日志文件
    open(log_path, 'w').close()

    # 输出日志切割完成的信息
    print(f"日志切割完成：{file_name} -> {os.path.basename(new_file_name)}")

# 读取配置文件
with open("config_date.txt", "r") as config_file:
    for line in config_file:
        # 解析配置项
        log_path, output_path = line.strip().split(',')

        split_log_by_date(log_path, output_path)
