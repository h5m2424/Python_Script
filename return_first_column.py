def get_first_column(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        first_column = [line.split()[0] for line in lines]
    return first_column

# 配置参数
input_file_path = 'input.txt'
output_file_path = 'output.txt'

# 调用函数获取第一列文本
first_column = get_first_column(input_file_path)

# 将结果输出到另一个文本文件中
with open(output_file_path, 'w') as output_file:
    for item in first_column:
        output_file.write(item + '\n')

# 打印第一列文本
print(f"结果已经写入到文本：{output_file_path}")
