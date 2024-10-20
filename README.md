# Lanzou Cloud Batch Downloader

[English](README.md) | [简体中文](README_CN.md)

A Python script for batch downloading files from Lanzou Cloud (蓝奏云).

For a detailed introduction to the project, please see my blog post: [Pi3's Notes](https://blog.pi3.fun/post/2023/09/python%E7%88%AC%E8%99%AB%E4%B9%8B%E8%93%9D%E5%A5%8F%E4%BA%91%E6%96%87%E4%BB%B6%E6%89%B9%E9%87%8F%E4%B8%8B%E8%BD%BD/)

## Features

- Supports downloading from multiple Lanzou Cloud links
- Handles password-protected links
- Creates separate folders for each download link
- Utilizes multi-threading for faster downloads
- Customizable download path

## Requirements

- Python 3.x
- Required Python packages:
  - requests
  - beautifulsoup4

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Pi3-l22/Lanzou_Download.git
   ```
2. Install the required packages:
   ```bash
   pip install requests beautifulsoup4
   ```

## Usage

1. Edit the `download_path` in `main.py` to set your desired download location:
   ```python
   download_path = r'D:\LanzouDownloads\\'
   ```

2. Create a text file named `File_Link.txt` in the same directory as `main.py`. Format the file as follows:
   ```bash
   Title1[FolderName1]
   https://wwvd.lanzoul.com/b030ok9y
   密码:9cj9
   Title2[FolderName2]
   https://wwvd.lanzoul.com/b030q0ge
   密码:hktq
   ```

3. Run the script:
   ```bash
   python main.py
   ```

## How It Works

1. The script reads the Lanzou Cloud links and passwords from the text file.
2. For each link, it:
   - Retrieves necessary parameters from the webpage
   - Sends a POST request to get file IDs and names
   - Obtains download URLs for each file
   - Creates a folder for the download
   - Uses multi-threading to download all files in parallel

## Note

This script is for educational purposes only. Please respect the terms of service of Lanzou Cloud and the copyright of the files you're downloading.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
