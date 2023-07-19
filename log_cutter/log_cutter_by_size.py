import os
import datetime

def convert_to_bytes(size):
    # 将大小转换为字节数
    kb_size = int(float(size) * 1024)
    return kb_size * 1024

def split_log_by_size(log_path, output_path, size, log_name):
    # 将大小转换为字节数
    size_in_bytes = convert_to_bytes(size)

    # 获取当前日期
    current_date = datetime.datetime.now().date()

    # 构造切割日期
    split_date = current_date.strftime("%Y-%m-%d")

    # 构造切割后的文件名
    file_name, file_ext = os.path.splitext(os.path.basename(log_path))
    new_file_name = os.path.join(output_path, f"{split_date}_{log_name}_part1{file_ext}")

    with open(log_path, 'rb') as file:
        chunk = file.read(size_in_bytes)

        # 判断第一个切片的大小是否满足切割标准
        if len(chunk) < size_in_bytes:
            print(f"{log_name} 日志大小小于切割标准")
            return

        part_num = 1

        while True:
            with open(new_file_name, 'wb') as part_file:
                part_file.write(chunk)

            part_num += 1
            new_file_name = os.path.join(output_path, f"{split_date}_{log_name}_part{part_num}{file_ext}")

            chunk = file.read(size_in_bytes)

            if not chunk:
                break

    # 清空原日志文件
    open(log_path, 'w').close()

    # 输出日志切割完成的信息
    print(f"{log_name} 日志切割完成")

# 读取配置文件
with open("config_size.txt", "r") as config_file:
    for line in config_file:
        # 解析配置项
        log_path, output_path, split_param = line.strip().split(',')

        log_name = os.path.splitext(os.path.basename(log_path))[0]
        size = float(split_param)
        split_log_by_size(log_path, output_path, size, log_name)
