# 日志分析器（Log-analysis）

一个只用 Python 标准库写的简易 Web 访问日志分析脚本。它逐行读取 `server.log` 这类访问日志，解析出时间、来源 IP、请求行和状态码，做访问频次统计，并把状态码 ≥ 400 的请求单独挑出来写入 `error.log`。

## 功能

- 逐行解析日志，跳过空行和格式不符的行，并统计跳过的行数
- 统计来源 IP、请求路径、状态码各自的访问频次
- 把状态码 ≥ 400 的请求写入 `error.log`
- 输出访问次数最多的 IP
- 生成 `record.log` 统计报告，按频次降序排列
- `CatchLog.read_log(limit=100)` 可预览日志的前 N 行

## 日志格式

每行由 `|` 分隔成四段，末尾可带换行：

```text
2026-11-14 10:00:01 | 192.168.1.10 | GET /api/words | 200
```

| 字段 | 说明 |
| --- | --- |
| 时间 | `YYYY-MM-DD HH:MM:SS` |
| IP | 来源地址 |
| 请求 | HTTP 方法与请求路径 |
| 状态码 | 三位数字 |

不符合该格式的行会被计为「无法解析的行」并跳过，不会中断程序。

## 使用方法

需要 Python 3，无第三方依赖。

```bash
python 日志分析.py
```

脚本用 `CatchLog(file_path, error_path, record_path)` 接收三个路径，分别对应输入日志、错误日志、统计报告。

注意：`__main__` 里写的是作者本机的绝对路径：

```python
catch = CatchLog('D:/code/programming-language/Python/日志分析器/server.log',
                 'D:/code/programming-language/Python/日志分析器/error.log',
                 'D:/code/programming-language/Python/日志分析器/record.log')
```

换到别的机器或目录运行时，请把这三处改成自己的路径（或改成相对路径），否则程序会提示「日志文件不存在」。

### 输出示例

```text
跳过无法解析的行: 0
访问最多的 IP 是: 192.168.1.10，共 12 次
```

同时在指定目录生成两个文件：

- `error.log`：状态码 ≥ 400 的原始日志行
- `record.log`：统计概览，以及 IP、状态码、请求路径的频次排行

## 运行时的文件

```text
.
├── 日志分析.py   # 主脚本
├── server.log    # 输入日志（示例数据）
├── error.log     # 运行后生成
└── record.log    # 运行后生成
```

## 主要方法

| 方法 | 作用 |
| --- | --- |
| `run_catch()` | 入口：校验路径、解析日志、统计并写报告 |
| `read_log(limit)` | 预览日志前 `limit` 行 |
| `write_in_record()` | 把统计结果写入 `record.log` |
| `find_most_frequent_ip()` | 返回访问次数最多的 IP |
