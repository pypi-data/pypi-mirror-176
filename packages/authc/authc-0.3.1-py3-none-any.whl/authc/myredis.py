import codefast as cf
from redis import StrictRedis

from authc.core import gunload as load


def get_redis_lab():
    # use TCP forward service to speed up redis connection
    l = cf.lis(['main_redis_host', 'main_redis_port',
                'main_redis_password']).map(load)
    return StrictRedis(host=l.first, port=l.second, password=l.last)


def get_redis():
    l = cf.lis(['redis_host', 'redis_port', 'redis_pass']).map(load)
    return StrictRedis(host=l.first, port=l.second, password=l.last)


def get_redis_cn():
    return get_redis()


def scf():
    """ Redis based on tencent scf
    """
    class ScfRedis(object):
        def __init__(self) -> None:
            self.url = (
                'aHR0cHM6Ly9zZXJ2aWNlLW81MXdqaHpkLTEzMDM5ODgwNDEuYmouYXBpZ'
                '3cudGVuY2VudGNzLmNvbS9yZWRpcwo=')
            self.url = cf.b64decode(self.url)
            self.headers = {'Content-Type': 'application/json'}

        def get(self, key: str) -> str:
            try:
                return cf.net.post(self.url, json={
                    'key': key
                }).json()['data']['value']
            except Exception as e:
                return None

        def set(self, key: str, value: str) -> None:
            return cf.net.post(self.url, json={'key': key, 'value': value})

        def exists(self, key: str) -> bool:
            return self.get(key) != None

    return ScfRedis()


class _Clients(object):
    @property
    def us(self):
        return get_redis()

    @property
    def cn(self):
        return get_redis_cn()

    @property
    def scf(self):
        return scf()

    @property
    def lab(self):
        return get_redis_lab()

    @property
    def local(self):
        return StrictRedis(host='localhost', port=6379, password=None)


rc = _Clients()
