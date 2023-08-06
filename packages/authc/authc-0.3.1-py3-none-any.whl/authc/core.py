import os
from typing import Any, Dict

import codefast as cf


def authc_fernet() -> Dict[str, str]:
    """ A new authc API based on fernet encryption
    """
    try:
        fernet_key = b'ArUB2LxWXnrdH5R2oUiAdiGGrHAB5mkRElTSuIoGGEc='
        paths = [
            os.path.join(os.path.expanduser("~"), '.config/textauth_fernet'),
            '/data/textauth_fernet', 'textauth_fernet'
        ]
        try:
            from cryptography.fernet import Fernet
        except ImportError:
            cf.warning('Fernet is not installed')
            cf.shell('pip3 install cryptography')

        f = Fernet(fernet_key)
        for p in paths:
            if cf.io.exists(p):
                js = f.decrypt(cf.io.reads(p).encode()).decode()
                return dict((k, v) for k, v in (x.split(':', 1)
                                                for x in js.split('\n') if x))
    except Exception as e:
        cf.error(e)
        return {}


def authc_openssl() -> Dict[str, str]:
    try:
        KEY = 'bDVlQnR2ZTdtM1MzcjZnVAo'
        paths = [
            os.path.join(os.path.expanduser("~"), '.config/textauth'),
            '/data/textauth', 'textauth'
        ]
        return cf.l(paths)\
            .filter(os.path.exists)\
            .map(lambda p: f'openssl bf -iter 1024 -d -k {KEY} < {p}')\
            .map(cf.shell)\
            .slice(0, 1)\
            .fmap(str.split, '\n')\
            .flatten()\
            .fmap(str.split, ':', 1)\
            .on_empty(cf.error, 'No such file: textauth').to_dict()
    except Exception as e:
        cf.error(e)
        return {}


def authc():
    fernet = authc_fernet()
    return fernet if fernet else authc_openssl()


def stdout() -> None:
    cf.dic(authc()).consume(lambda p: print(f'{p[0]:<30}: {p[1]}'))


class Gunloader(object):
    def __init__(self) -> None:
        self._accs = None

    @property
    def accs(self):
        if self._accs is None:
            self._accs = authc()
        return self._accs

    def __call__(self, key: str, *args: Any, **kwds: Any) -> Any:
        return cf.dic(self.accs).filter_keys([key]).on_empty(
            cf.warning, f'NO such key: {key} found in authc').lvalues().first


gunload = Gunloader()
