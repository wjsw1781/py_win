# encoding=utf-8
import m3u8
import requests
import datetime
import os
from Crypto.Cipher import AES
from Crypto import Random
import glob
# Request header, not necessary, see website change
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
"""
 pip install pycryptodome  -i https://pypi.tuna.tsinghua.edu.cn/simple 

"""

 
 
def download(ts_urls, download_path, keys=[]):
    if not os.path.exists(download_path):
        os.mkdir(download_path)
 
    decrypt = True
    if len(keys )== 0 :  # m3u8 will get [None] if not key or []
        decrypt = False
 
    for i in range(len(ts_urls)):
        ts_url = ts_urls[i]
        file_name = 'https://v4-vod.kwaicdn.com/ksc2/'+ts_url.uri
        print("start download %s" %file_name)
        start = datetime.datetime.now().replace(microsecond=0)
        try:
            response = requests.get(file_name, stream=True, verify=False)
        except Exception as e:
            print(e)
            raise ValueError('某个片段失败')
         
 
        ts_path = download_path+"/{0}.ts".format(i)
        if decrypt:
            key = keys[i]
            iv = Random.new().read(AES.block_size)
            cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC)
 
        with open(ts_path,"wb+") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    if decrypt:
                        file.write(cryptor.decrypt(chunk))
                    else:
                        file.write(chunk)
 
        end = datetime.datetime.now().replace(microsecond=0)
        print("total time：%s"%(end-start))
 
 
def merge_to_mp4(dest_file, source_path, delete=False):
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
    with open(dest_file, 'wb') as fw:
        files = glob.glob(source_path + '/*.ts')
        for file in files:
            with open(file, 'rb') as fr:
                fw.write(fr.read())
                print(f'\r{file} Merged! Total:{len(files)}', end="     ")
            os.remove(file)
 
def m3u8_to_mp4(m3u8_url, output_file, decrypt=False, keys=None):
    m3u8_file='./key.m3u8'
    with open(m3u8_file, 'wb') as ff:
        ff.write(requests.get(m3u8_url).content)
    video = m3u8.load(m3u8_file)
    download(video.segments, 'tmp', [])
    merge_to_mp4(output_file, 'tmp')
    pass

if __name__ == "__main__":
    url = "https://v4-vod.kwaicdn.com/ksc2/a7IPRdpwwpT4cuTdTC33aSY0ClR0MOfdlCyJm-OJT9IldEPjbl7XruOyDfbUIJdjxRINYMZCNfWUYRcFx_r52Q.m3u8?pkey=AAVffduyGsJvEXURqDixwTWB195wc_UjhnTsgyJvBUQkWBDQbBqNvP-FwY9vQ2-GFd5Ao_vLGobwVTEuR_rx5OdQ3WwuEv_pzhQ0fTaUbNuDAncLrHwNVdQHs7TO6C02pTQ&ss=vp"
    m3u8_file='./key.m3u8'
    with open(m3u8_file, 'wb') as ff:
        ff.write(requests.get(url).content)
    video = m3u8.load(m3u8_file)
    print(video.data)
    download(video.segments, 'tmp', [])
    merge_to_mp4('result.mp4', 'tmp')