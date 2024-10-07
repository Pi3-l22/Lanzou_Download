import requests
from bs4 import BeautifulSoup
import json
import os
from multiprocessing.pool import Pool

download_path = r'D:\文件下载地址\\'


# 整理链接地址
def get_url_data():
    fp = open('File_Link.txt', 'r', encoding='utf-8')
    lines = fp.readlines()
    fp.close()
    url = []
    password = []
    dir_name = []
    for line in lines:
        if line[0] == 'h':
            url.append(line.strip())  # 去除结尾换行符
        elif line.startswith('密码'):
            password.append(line.strip()[3:])
        else:
            dir_name.append(line.strip()[:-1])
    return url, password, dir_name


def get_key(url: str):
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.find('div', attrs={'class': 'd', 'id': 'info'})  # 获取到div标签
    script = div.next_sibling.next_sibling  # 获取下一个兄弟节点 即script
    # print(script)
    # var ibf1fz = '1693922274';
    # var _hddhs = 'c5010165681fd1c5fd8be8a4bcf20906';
    # 获取ibf1fz和_hddhs
    ibf1fz = script.string.split(';')[5].split('=')[1][2:-1]
    hddhs = script.string.split(';')[6].split('=')[1][2:-1]
    # fid: 4805955
    # uid: 2427876
    # 获取fid和uid
    fid = script.string.split(',')[3].split(':')[1]
    uid = script.string.split(',')[4].split(':')[1][1:-1]
    return ibf1fz, hddhs, fid, uid


def get_download_id(t: str, k: str, f: str, u: str, pwd: str):
    # 请求表单数据
    data = {
        'lx': '2',
        'fid': f,
        'uid': u,
        'pg': '1',
        'rep': '0',
        't': t,  # 当前时间戳
        'k': k,  # 感觉应该是32位md5加密后的密码 可以从网页源码中找到
        'up': '1',
        'ls': '1',
        'pwd': pwd
    }
    response = requests.post(url=source_url, data=data, headers=headers)
    # print(response.text)
    # 返回数据为json格式，我们要提取里面id的值
    # print(response.json())
    download_id = []
    file_name_all = []
    download_id_lists = response.json()['text']
    for data_dict in download_id_lists:
        download_id.append(data_dict['id'])
        file_name_all.append(data_dict['name_all'])
    # print(download_id)
    # print(file_name_all)
    return download_id, file_name_all


def get_ajaxdata(download_url: str):
    response = requests.get(url=download_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_btn_url = lanzou_url + soup.find('iframe', attrs={'class': 'ifr2'})['src']
    # print(download_btn_url)
    # TODO 用request请求返回浏览器渲染之前的网页源码，没有包含文件下载地址
    # TODO 用selenium模拟浏览器请求，但是速度太慢了，而且还要安装chromedriver.exe
    # TODO 可以直接请求 ajaxm.php 文件，里面返回了文件下载地址
    response = requests.get(url=download_btn_url, headers=headers, timeout=10000)
    response.encoding = 'utf-8'  # 防止中文乱码
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    script = soup.find('div', attrs={'class': 'load'}).nextSibling.nextSibling
    # print(script)
    # 获取各个元素的值
    # wsk_sign = script.string.split(';')[0].split('=')[1][2:-1]
    aihidcms = script.string.split(';')[1].split('=')[1][2:-1]
    iucccjdsd = script.string.split(';')[2].split('=')[1][2:-1]
    # ws_sign = script.string.split(';')[3].split('=')[1][2:-1]
    start_index = script.string.find("'sign':") + len("'sign':")
    end_index = script.string.find(",", start_index)
    sasign = script.string[start_index:end_index].strip().strip("'")
    ajaxdata = script.string.split(';')[5].split('=')[1][2:-1]
    # print(aihidcms, iucccjdsd, sasign, ajaxdata)
    return aihidcms, iucccjdsd, sasign, ajaxdata


def thread_download_file(file_url, file_name, dir_name: str):
    data = {
        '': file_url.rsplit('/')[-1].replace('?', '').replace('=', ':')
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'down_ip=1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }
    file = requests.get(url=file_url, headers=headers, data=data).content
    with open(download_path + dir_name + '/' + file_name, 'wb') as file_down:
        file_down.write(file)
        file_down.close()
        print(file_name + ' ----- 下载完成！')
    # with open(dir_name + '/' + file_name_all[0], 'wb') as fp:
    #     for chunk in response.iter_content(chunk_size=102400):
    #         if chunk:
    #             fp.write(chunk)


def download_file(download_id: list, dir_name: str, file_name_all: list):
    # 创建文件夹
    if not os.path.exists(download_path + dir_name):  # 是否存在文件夹
        os.mkdir(download_path + dir_name)
        print(dir_name + ' ----- 文件夹创建成功！')
    # 文件直链列表
    file_url_list = []
    for j in range(len(download_id)):
        # for j in range(1):
        download_url = lanzou_url + '/' + download_id[j]
        # print(download_url)
        request_url = 'https://wwr.lanzoui.com/ajaxm.php'
        aihidcms, iucccjdsd, sasign, ajaxdata = get_ajaxdata(download_url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': download_url
        }
        data = {
            'action': 'downprocess',
            'signs': ajaxdata,
            'sign': sasign,
            'websign': iucccjdsd,
            'websignkey': aihidcms,
            'ves': '1'
        }
        response = requests.post(url=request_url, data=data, headers=headers)
        # 转为字典格式
        response_dict = json.loads(response.text)
        # 拼接成文件的链接地址
        file_url_list.append(response_dict['dom'] + '/file/' + response_dict['url'])
        # print(file_url_list)
        # 请求文件直链下载文件
        # 链接被重定向了，需要设置allow_redirects=True
        # response = requests.get(url=file_url_list[0], headers=headers, timeout=10)
        # web.get('chrome').open(file_url_list[0])
    # 多线程池 并行下载
    pool = Pool(16)  # 创建一个进程池，最大进程数为16
    for i in range(len(file_url_list)):
        pool.apply_async(thread_download_file, args=(file_url_list[i], file_name_all[i], dir_name))
    pool.close()
    pool.join()


if __name__ == '__main__':
    source_url = 'https://wwr.lanzoui.com/filemoreajax.php'
    lanzou_url = 'https://wwr.lanzoui.com'
    url, password, dir_name = get_url_data()
    for i in range(len(url)):
        # for i in range(1):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': url[i]
        }
        ibf1fz, hddhs, fid, uid = get_key(url[i])
        # print(ibf1fz, _hddhs, fid, uid)
        download_id, file_name_all = get_download_id(ibf1fz, hddhs, fid, uid, password[i])
        # 下载文件
        download_file(download_id, dir_name[i], file_name_all)
