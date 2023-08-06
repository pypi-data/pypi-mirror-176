import asyncio
import copy
import json
import datetime
import traceback
import requests as sync_requests
from aiohttp_requests import requests, Requests
from aiohttp import ClientResponse
from urllib.parse import urlparse
from CrawlSpider.Utils.SplashHandler import webSplash

requests:Requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
}



class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8', 'ignore')
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



class SpiderRequest:
    async def requestAsync(self,method, url, form="content", **kwargs):
        h = {}
        h.update(headers)
        _headers: dict = 'headers' in kwargs and kwargs.pop('headers')
        if not isinstance(_headers, dict):
            _headers = {}
        h.update(_headers)

        'chrome_options' in kwargs and kwargs.pop('chrome_options')
        r = None
        retry = 'retry' in kwargs and kwargs.pop('retry') or 3
        status_code = 200
        closeFlag = 1
        while retry:
            try:
                # resp: ClientResponse = await request.session.get(url, headers=_headers, **kwargs)
                resp: ClientResponse = await requests.session.request(method, url, headers=h, **kwargs)
                status_code = resp.status
                if resp and resp.ok:
                    if form == 'json':
                        r = await resp.json()
                    elif form == 'text':
                        r = await resp.text()
                    elif form == 'content':
                        r = await resp.read()
                    elif form == 'origin':
                        r = resp
                        closeFlag = 0
                    if closeFlag:
                        resp.close()
                    break
                elif 400<status_code<500:
                    r = resp
                    resp.close()
                    break
                else:
                    retry -= 1
                    r = await resp.json()
            except Exception as e:
                print("url请求报错:", url)
                print(e)
                retry -= 1
                status_code = 500


        return {
            'status_code': status_code,
            'content': r
        }

    async def requestSync(self,method, url, form="content", **kwargs):
        h = {}
        h.update(headers)
        _headers: dict = 'headers' in kwargs and kwargs.pop('headers')
        if not isinstance(_headers, dict):
            _headers = {}
        h.update(_headers)

        'chrome_options' in kwargs and kwargs.pop('chrome_options')


        proxyUrl = (kwargs.get('proxy') and kwargs.pop('proxy')) or ""
        if proxyUrl:
            res = urlparse(proxyUrl)
            proxies = {
                res.scheme: res.netloc
            }
            kwargs['proxies'] = proxies
        resp = sync_requests.request(method, url, headers=h, **kwargs)
        r = None
        status_code = resp.status_code
        if resp and resp.ok:  # 注意这里是status，不是status_code
            if form == 'json':
                r = resp.json()
            elif form == 'text':
                r = resp.text
            elif form == 'content':
                r = resp.content
            elif form == 'origin':
                r = resp
        return {
            'status_code': status_code,
            'content': r
        }


    async def getAsync(self,url, form="content", **kwargs):
        h = {}
        h.update(headers)
        _headers: dict = 'headers' in kwargs and kwargs.pop('headers')
        if not isinstance(_headers, dict):
            _headers = {}
        h.update(_headers)

        'chrome_options' in kwargs and kwargs.pop('chrome_options')
        r = None
        retry = 3
        status_code = 200
        closeFlag = 1
        while retry:
            try:
                resp: ClientResponse = await requests.session.get(url, headers=h, **kwargs)
                status_code = resp.status
                if resp and resp.ok:
                    if form == 'json':
                        r = await resp.json()
                    elif form == 'text':
                        r = await resp.text()
                    elif form == 'content':
                        r = await resp.read()
                    elif form == 'origin':
                        r = resp
                        closeFlag = 0
                    if closeFlag:
                        resp.close()
                    break
                else:
                    retry -= 1
            except Exception as e:
                print("url请求报错:", url)
                print(e)
                retry -= 1
                status_code = 500

        return {
            'status_code': status_code,
            'content': r
        }


    async def getSync(self,url, form="content", **kwargs):
        h = {}
        h.update(headers)
        _headers: dict = 'headers' in kwargs and kwargs.pop('headers')
        if not isinstance(_headers, dict):
            _headers = {}
        h.update(_headers)

        'chrome_options' in kwargs and kwargs.pop('chrome_options')


        proxyUrl = (kwargs.get('proxy') and kwargs.pop('proxy')) or ""
        if proxyUrl:
            res = urlparse(proxyUrl)
            proxies = {
                res.scheme: res.netloc
            }
            kwargs['proxies'] = proxies
        resp = sync_requests.get(url, headers=h, **kwargs)
        r = None
        status_code = resp.status_code
        if resp and resp.ok:  # 注意这里是status，不是status_code
            if form == 'json':
                r = resp.json()
            elif form == 'text':
                r = resp.text
            elif form == 'content':
                r = resp.content
            elif form == 'origin':
                r = resp
        return {
            'status_code': status_code,
            'content': r
        }


    async def postAsync(self, url, form="content", **kwargs):
        h = {}
        h.update(headers)
        _headers: dict = 'headers' in kwargs and kwargs.pop('headers')
        if not isinstance(_headers, dict):
            _headers = {}
        h.update(_headers)

        'chrome_options' in kwargs and kwargs.pop('chrome_options')
        r = None
        retry = 3
        status_code = 200
        closeFlag = 1
        while retry:
            try:
                resp: ClientResponse = await requests.session.post(url, headers=h, **kwargs)
                status_code = resp.status
                if resp and resp.ok:  # 注意这里是status，不是status_code
                    if form == 'json':
                        r = await resp.json()
                    elif form == 'text':
                        r = await resp.text()
                    elif form == 'content':
                        r = await resp.read()
                    elif form == 'origin':
                        r = resp
                        closeFlag = 0
                    if closeFlag:
                        resp.close()

                    break
                else:
                    retry -= 1
            except Exception as e:
                print("url请求报错:", url)
                print(e)
                retry -= 1
                status_code = 500
        return {
            'status_code': status_code,
            'content': r
        }

    async def postSync(self, url, form="content", **kwargs):
        h = {}
        h.update(headers)
        _headers: dict = 'headers' in kwargs and kwargs.pop('headers')
        if not isinstance(_headers, dict):
            _headers = {}
        h.update(_headers)

        'chrome_options' in kwargs and kwargs.pop('chrome_options')

        proxyUrl = (kwargs.get('proxy') and kwargs.pop('proxy')) or ""
        if proxyUrl:
            res = urlparse(proxyUrl)
            proxies = {
                res.scheme: res.netloc
            }
            kwargs['proxies'] = proxies
        resp =  sync_requests.post(url, headers=h, **kwargs)
        r = None
        status_code = resp.status_code

        if resp.ok:  # 注意这里是status，不是status_code
            if form == 'json':
                r = resp.json()
            elif form == 'text':
                r = resp.text
            elif form == 'content':
                r = resp.content
            elif form == 'origin':
                r = resp

        return {
            'status_code': status_code,
            'content': r
        }

    async def get(self, url, isAllow302=True, isUsingProxy=False, isSplash=False, **kwargs):
        if isUsingProxy:
            ret = await self.proxy(self.get_, url, isAllow302=isAllow302, isSplash=isSplash, **kwargs)
        else:
            ret = await self.get_(url, isAllow302=isAllow302, isSplash=isSplash,**kwargs)
        return ret

    async def get_(self, url, isAllow302=True,  isSplash=False,isAsync=True, **kwargs):
        if isSplash:
            return await self.splash(url, **kwargs)
        elif isAsync:
            ret = await self.getAsync(url, **kwargs)
            return ret
        elif not isAsync:
            return await self.getSync(url, **kwargs)

    @classmethod
    async def splash(cls,url, **kwargs):
        loop = asyncio.get_running_loop()
        # --proxy-server=socks5://xxx.xxx:xxx
        options = kwargs.get('chrome_options')
        splashTime = kwargs.get('splashTime') or 0.2
        isUsingNewDriver = kwargs.get('isUsingNewDriver')
        driver = None
        if isUsingNewDriver:
            driver = webSplash.getNewDriver(options)
        elif options:
            driver = webSplash.getDriver(options=options)
        future = loop.run_in_executor(None, webSplash.getSource, url, driver, splashTime)
        res = await future
        return res

    @classmethod
    def splashSync(cls, url, **kwargs):
        options = kwargs.get('chrome_options')
        splashTime = kwargs.get('splashTime') or 0.2
        isUsingNewDriver = kwargs.get('isUsingNewDriver')
        driver = None
        if isUsingNewDriver:
            driver = webSplash.getNewDriver(options)
        elif options:
            driver = webSplash.getDriver(options=options)
        res = webSplash.getSource(url, driver, splashTime)
        return res


    @classmethod
    async def proxy(cls,fn, url, isAllow302=True,  isSplash=False, **kwargs):
        from CrawlSpider.Utils.RetrieveProxy import RetrieveProxy
        _kwargs = copy.deepcopy(kwargs)
        isFree = True
        proxyType = _kwargs.pop('proxyType') if 'proxyType' in _kwargs else 'abuyun'
        protocol = _kwargs.pop('protocol') if 'protocol' in _kwargs else 'http'
        if 'isFree' in _kwargs:
            isFree = _kwargs.pop('isFree')
        if isFree:
            retry = 3
            proxy, _ = await RetrieveProxy.getProxyFree()
            print("获取到的免费代理IP:", proxy)
            # proxies requests {}
            httpProxy = f"{protocol}://{proxy}"
            _kwargs.update({
                'proxy': httpProxy,
                'chrome_options': [f'--proxy-server={httpProxy}']
            })
            while retry:
                try:
                    ret = await fn(url, isAllow302=isAllow302, isSplash=isSplash, **_kwargs)
                    return ret
                except Exception as e:
                    print("e", e)
                    retry -= 1
            ret = await RetrieveProxy.delete(proxy)
            print("删除结果:", ret)
        proxy, _ = await RetrieveProxy.getProxy(proxyType=proxyType)

        if proxy:

            httpProxy = f"{protocol}://{proxy}" if not proxy.startswith(protocol) else proxy

            _kwargs.update({
                'proxy': httpProxy,
                'chrome_options': [f'--proxy-server={httpProxy}']
            })
            try:
                ret = await fn(url, isAllow302=isAllow302, isSplash=isSplash, **_kwargs)
                return ret
            except Exception as e:
                print("e", e)
                return None


    async def post(self, url, isAllow302=True, isUsingProxy=False, isSplash=False,**kwargs):
        if isUsingProxy:
            ret = await self.proxy(self.post_, url, isAllow302=isAllow302, isSplash=isSplash, **kwargs)
        else:
            ret = await self.post_(url, isAllow302=isAllow302, isSplash=isSplash, **kwargs)

        return ret

    async def post_(self, url, isAllow302=True, isSplash=False,isAsync=True,**kwargs):
        if isAsync:
            ret = await self.postAsync(url,  **kwargs)
        else:
            ret = await self.postSync(url,  **kwargs)
        return ret
    @classmethod
    def toJson(cls, data,**kwargs):
        return json.dumps(data, ensure_ascii=False, cls=MyEncoder, **kwargs)
    @classmethod
    def fromJson(cls, data, encoding='utf-8', **kwargs):
        return json.loads(data, encoding=encoding, **kwargs)


spiderRequest = SpiderRequest()
