import time
from curl_cffi import requests


# a small session that keeps the browser TLS fingerprint (via impersonate),
# rotates a proxy if you pass one, and retries on 5xx/network errors.
class Client:
    def __init__(self, impersonate="chrome", proxy=None, retries=3, timeout=20):
        self.impersonate = impersonate
        self.proxy = proxy
        self.retries = retries
        self.timeout = timeout
        self.s = requests.Session()

    def get(self, url, **kw):
        proxies = None
        if self.proxy:
            proxies = {"http": self.proxy, "https": self.proxy}

        last = None
        for i in range(self.retries):
            try:
                r = self.s.get(url, impersonate=self.impersonate,
                               proxies=proxies, timeout=self.timeout, **kw)
                if r.status_code < 500:
                    return r
                last = f"status {r.status_code}"
            except Exception as e:
                last = str(e)
            time.sleep(0.5 * 2 ** i)

        raise RuntimeError(f"failed after {self.retries} tries: {last}")
