import re
from collections import Counter
from pathlib import Path

# 日志样例
# 2026-11-14 10:00:01 | 192.168.1.10 | GET /api/words | 200

LOG_PATTERN = re.compile(
    r'^(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    r'\s*\|\s*(?P<ip>[\d.]+)'
    r'\s*\|\s*(?P<request>.+?)'
    r'\s*\|\s*(?P<code>\d+)\s*$'
)

class CatchLog():
    # 初始化对象
    def __init__(self, file_path, error_path, record_path):
        self.bad_lines = 0
        self.file_path = file_path
        self.error_path = error_path
        self.record_path = record_path
        self.code_freq = Counter()
        self.req_freq = Counter()
        self.ip_freq = Counter()

    # 输出日志
    def read_log(self, limit=100):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= limit:
                    print(f"...（仅显示前 {limit} 行）")
                    break
                print(line, end='')

    # 找出读取最多的IP
    def find_most_frequent_ip(self):
        top = self.ip_freq.most_common(1)
        return top[0][0] if top else None

    # 将各个参数频次存入record
    def write_in_record(self):
        if not Path(self.record_path).parent.exists():
            print(f"记录文件目录不存在: {Path(self.record_path).parent}")
            return
        total = sum(self.ip_freq.values())
        try:
            with open(self.record_path, 'w', encoding='utf-8') as rec:
                rec.write(f"=== 统计概览 ===\n")
                rec.write(f"有效行数: {total}\n")
                rec.write(f"跳过无法解析的行: {self.bad_lines}\n\n")
                rec.write(f"=== IP 访问频次（降序） ===\n")
                for ip, cnt in self.ip_freq.most_common():
                    rec.write(f"{ip}: {cnt}\n")
                rec.write("\n")
                rec.write(f"=== 状态码频次（降序） ===\n")
                for code, cnt in self.code_freq.most_common():
                    rec.write(f"{code}: {cnt}\n")
                rec.write("\n")
                rec.write(f"=== 请求路径频次（降序） ===\n")
                for req, cnt in self.req_freq.most_common():
                    rec.write(f"{req}: {cnt}\n")
        except OSError as e:
            print(f"写入记录文件失败: {e}")
    
    # 调用对象入口
    def run_catch(self):
        if not Path(self.file_path).exists():
            print(f"日志文件不存在: {self.file_path}")
            return
        if not Path(self.error_path).parent.exists():
            print(f"错误日志目录不存在: {Path(self.error_path).parent}")
            return
        if not Path(self.record_path).parent.exists():
            print(f"记录文件目录不存在: {Path(self.record_path).parent}")
            return

        # 状态更新
        self.bad_lines = 0
        self.code_freq = Counter()
        self.req_freq = Counter()
        self.ip_freq = Counter()
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as log ,\
                 open(self.error_path, 'w', encoding='utf-8') as err:
                # 逐行读入
                for line in log:
                    # 校验段
                    line = line.rstrip('\n')
                    if not line:
                        continue
                    m = LOG_PATTERN.match(line)
                    if not m:
                        self.bad_lines += 1
                        continue
                    req = m.group('request')
                    ip = m.group('ip')
                    code = int(m.group('code'))
                    # 写入状态非200的字段v
                    if code >= 400:
                        err.write(line + '\n')
                    # 统计各参数访问次数
                    self.ip_freq[ip] += 1
                    self.req_freq[req] += 1
                    self.code_freq[code] += 1

        # except
        except OSError as e:
            print(f"文件读写失败: {e}")
            return
        
        # 无法解析的行数
        print(f"跳过无法解析的行: {self.bad_lines}")
        
        # 输出最多访问的ip
        ip = self.find_most_frequent_ip()
        if ip is None:
            print("日志为空，无有效记录")
        else:
            print(f"访问最多的 IP 是: {ip}，共 {self.ip_freq[ip]} 次")

        # 写入record
        self.write_in_record()

# 跑主函数
if __name__ == '__main__':
    catch = CatchLog('D:/code/programming-language/Python/日志分析器/server.log', 
                    'D:/code/programming-language/Python/日志分析器/error.log',
                    'D:/code/programming-language/Python/日志分析器/record.log')
    catch.run_catch()