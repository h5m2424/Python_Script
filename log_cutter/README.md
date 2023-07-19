### 功能介绍
* 根据日志大小或日期切割日志

### 脚本介绍
* log_cutter_by_size.py：把“需要切割的日志”，“切割后的日志存储路径”，“单个日志文件的大小（MB）”按顺序写入配置文件“config_size.txt”，逗号隔开，一行一个日志文件。如果需要按照KB切割可以填写小数（如0.5表示500KB）
* log_cutter_by_size.py：把“需要切割的日志”，“切割后的日志存储路径”按顺序写入配置文件“config_date.txt”，逗号隔开，一行一个日志文件。使用时可以结合crontab定期切割

### 使用方法
```bash
python3 log_cutter_by_date.py
```
```bash
python3 log_cutter_by_size.py
```
