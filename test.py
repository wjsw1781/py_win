


from loguru import logger
import httpx


def get_request(url, proxies=None, retries=3,**kargs):
    exception = None
    for i in range(retries):
        try:
            
            response = httpx.get(url, proxies=proxies,timeout=12,follow_redirects=True,**kargs)
            response.raise_for_status()  # 如果响应状态码不是 200，就抛出异常
            return response
        except Exception as e:
            exception = e
    logger.error(f'请求出错: {exception} {url}')
    return None

res=get_request('https://ipinfo.io/json')
print(res.text)


