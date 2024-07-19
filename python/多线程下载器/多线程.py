import threading
import http.client
from urllib.parse import urlparse

# 获取文件大小的函数
def get_file_size(url):
    # 解析URL
    parsed_url = urlparse(url)
    # 建立HTTPS连接
    conn = http.client.HTTPSConnection(parsed_url.netloc)
    try:
        # 发送HEAD请求以获取文件信息
        conn.request("HEAD", parsed_url.path)
        response = conn.getresponse()
        # 获取文件大小
        size = int(response.getheader('Content-Length'))
    except http.client.RemoteDisconnected:
        # 如果HEAD请求失败，使用GET请求获取文件大小
        conn.request("GET", parsed_url.path)
        response = conn.getresponse()
        # 获取文件大小
        size = int(response.getheader('Content-Length'))
    finally:
        # 关闭连接
        conn.close()
    return size

# 下载特定块的函数
def download_chunk(url, start, end, chunk_num, results):
    # 解析URL
    parsed_url = urlparse(url)
    # 设置Range头以请求特定字节范围
    headers = {'Range': f'bytes={start}-{end}'}
    # 建立HTTPS连接
    conn = http.client.HTTPSConnection(parsed_url.netloc)
    # 发送GET请求以下载特定字节范围的内容
    conn.request("GET", parsed_url.path, headers=headers)
    response = conn.getresponse()

    # 如果响应状态为206（部分内容）
    if response.status == 206:
        # 读取数据
        data = response.read()
        # 存储数据在结果列表中
        results[chunk_num] = data
        print(f"Downloaded chunk {chunk_num}")
    else:
        # 打印错误信息
        print(f"Failed to download chunk {chunk_num}, status code: {response.status}")

    # 关闭连接
    conn.close()

# 主函数
def main():
    # 下载文件的URL
    url = "https://dow.dowlz17.com/20240709/839_4c4f5460/%E4%B8%80%E5%BF%B5%E6%B0%B8%E6%81%92%E7%AC%AC3%E5%AD%A3_%E7%AC%AC5%E9%9B%86.mp4"
    # 获取文件大小
    file_size = get_file_size(url)
    # 定义每个块的大小（将文件分成4块）
    chunk_size = file_size // 4
    # 存储线程对象的列表
    threads = []
    # 存储下载结果的列表
    results = [None] * 4

    # 创建并启动线程，每个线程下载一个块
    for i in range(4):
        # 计算每个块的起始和结束位置
        start = i * chunk_size
        end = file_size - 1 if i == 3 else (i + 1) * chunk_size - 1
        # 创建线程对象
        thread = threading.Thread(target=download_chunk, args=(url, start, end, i, results))
        # 将线程添加到列表中
        threads.append(thread)
        # 启动线程
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 合并所有下载的块
    with open("downloaded_file.mp4", 'wb') as file:
        for chunk in results:
            file.write(chunk)

    print("All downloads completed.")

# 检查是否直接运行该脚本
if __name__ == "__main__":
    main()
