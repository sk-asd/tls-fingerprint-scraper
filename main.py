import json
from curl_cffi import requests

# public TLS inspector - echoes back the JA3 of whoever calls it.
ECHO = "https://tls.peet.ws/api/all"


def ja3(impersonate):
    kw = {"timeout": 20}
    if impersonate:
        kw["impersonate"] = impersonate
    d = requests.get(ECHO, **kw).json()
    tls = d.get("tls", {})
    return tls.get("ja3_hash") or tls.get("ja3") or "?"


# same request, three identities. the point: at the TLS layer a plain python
# client looks nothing like a browser, and anti-bot systems check exactly that.
# impersonate makes the handshake match a real chrome/safari.
if __name__ == "__main__":
    for name in [None, "chrome", "safari", "firefox"]:
        label = name or "no impersonate"
        try:
            print(f"{label:<16} {ja3(name)}")
        except Exception as e:
            print(f"{label:<16} error: {e}")
