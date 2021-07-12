# -*- coding: UTF-8 -*-
import os
import zipfile
import json
from os.path import dirname, isdir

import requests as requests


# 压缩目录  目前无用
def DirToZip(dir, zip_fp, delete=False):
    ''' 文件夹打包成zip
    :param dir:     r'C:\data'
    :param zip_fp:  r'C:\data.zip'
    :param delete:  True 删除原文件（可选）
    :return:
    '''
    if not zip_fp.endswith('zip'): return None  # 保存路径出错
    if not isdir(dirname(zip_fp)):
        print('cannot create zipfile because target does not exists')
        os.makedirs(dirname(zip_fp))
    fps = []
    zipf = zipfile.ZipFile(zip_fp, "w")  # 创建一个zip对象
    for root, dirs, fns in os.walk(dir):
        for fn in fns:
            fp = os.path.join(root, fn)
            arcname = fp.replace(dir, '')  # fn在dir中的相对位置
            zipf.write(fp, arcname)
            fps.append(fp)
    zipf.close()
    if delete:
        for fp in fps:
            os.remove(fp)
    return zip_fp


# 文件列表
def FilesToZip(fps, zip_fp, delete=False):
    ''' 多文件打包成zip
    :param fps:   [r'C:\1.txt', r'C:\2.txt', r'C:\3.txt'] 文件全路径的list
    :param zip_fp:  r'C:\files.zip'
    :param delete:  True    删除原文件
    :return:
    '''
    if len(fps) == 0: return None
    if not zip_fp.endswith("zip"): return None
    zipf = zipfile.ZipFile(zip_fp, "w")  # 在路径中创建一个zip对象
    for fp in fps:
        fn = os.path.basename(fp)
        zipf.write(fp, fn)  # 第一个参数为该文件的全路径；第二个参数为文件在zip中的相对路径
    zipf.close()  # 关闭文件
    if delete:  # 删除原文件
        for fp in fps:
            os.remove(fp)
    return zip_fp


def sendRequest(url, querystring):
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if not response.text:
        return None
    dat = json.loads(response.text)
    return dat


# 格式化json输出
def get_pretty_print(json_object):
    return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


if __name__ == '__main__':
    js = sendRequest("http://img.jiaoyuxueli.cn/api/?act=act1&t=1&sn=f9be311e65d81a9ad8150a60844bb94c", {})
    if js != None:
        pass
    print(js)
    id = js['id']
    fromdir = js['from']
    tofile = js['to']
    DirToZip(fromdir, tofile, False)
    # os.rmdir(fromdir)
    sendRequest("http://img.jiaoyuxueli.cn/api/?act=act1up&t=1&sn=f9be311e65d81a9ad8150a60844bb94c", {'id': id})
