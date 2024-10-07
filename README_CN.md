# 蓝奏云批量下载器

[English](README.md) | [简体中文](README_CN.md)

这是一个用于批量下载蓝奏云文件的Python脚本。

项目的详细介绍可以参见我的博客文章：[Pi3'Notes](https://blog.pi3.fun/post/2023/09/python%E7%88%AC%E8%99%AB%E4%B9%8B%E8%93%9D%E5%A5%8F%E4%BA%91%E6%96%87%E4%BB%B6%E6%89%B9%E9%87%8F%E4%B8%8B%E8%BD%BD/)

## 功能特点

- 支持从多个蓝奏云链接下载
- 处理带密码的链接
- 为每个下载链接创建单独的文件夹
- 使用多线程实现更快的下载速度
- 可自定义下载路径

## 环境要求

- Python 3.x
- 所需Python包：
  - requests
  - beautifulsoup4

## 安装

1. 克隆此仓库：
   ```
   git clone https://github.com/Pi3-l22/Lanzou_Download.git
   ```
2. 安装所需包：
   ```
   pip install requests beautifulsoup4
   ```

## 使用方法

1. 在`main.py`中编辑`download_path`以设置您想要的下载位置：
   ```python
   download_path = r'D:\蓝奏云下载文件\\'
   ```

2. 在与`main.py`相同的目录下创建一个名为`File_Link.txt`的文本文件。按以下格式编写文件内容：
   ```
   标题1[文件夹名称1]
   https://wwvd.lanzoul.com/b030ok9y
   密码:9cj9
   标题2[文件夹名称2]
   https://wwvd.lanzoul.com/b030q0ge
   密码:hktq
   ```

3. 运行脚本：
   ```
   python main.py
   ```

## 工作原理

1. 脚本从文本文件中读取蓝奏云链接和密码。
2. 对于每个链接，脚本会：
   - 从网页获取必要的参数
   - 发送POST请求以获取文件ID和名称
   - 获取每个文件的下载URL
   - 为下载创建一个文件夹
   - 使用多线程并行下载所有文件

## 注意事项

本脚本仅用于教育目的。请尊重蓝奏云的服务条款和您下载文件的版权。

## 许可证

本项目采用MIT许可证 - 详情请见[LICENSE](LICENSE)文件。
