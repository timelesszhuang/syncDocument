# -*- coding: UTF-8 -*-
import os
import zipfile
import json
import requests as requests


def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir):
        os.makedirs(unziptodir, 0o777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.mkdir(ext_dir, 0o777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()


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
    js = sendRequest("http://img.jiaoyuxueli.cn/api/?act=act2&t=1&sn=f9be311e65d81a9ad8150a60844bb94c", {})
    if js != None:
        pass
    print(js)
    id = js['id']
    fromfile = js['from']
    todir = js['to']
    unzip_file(fromfile, todir)
    # 删除文件
    # os.remove(fromfile)
    sendRequest("http://img.jiaoyuxueli.cn/api/?act=act2up&t=1&sn=f9be311e65d81a9ad8150a60844bb94c", {'id': id})
