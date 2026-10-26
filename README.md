# tls-fingerprint-scraper

A lot of anti-bot systems don't look at your headers first - they look at your
TLS handshake. A plain Python `requests` call has a JA3 fingerprint that no real
browser produces, so you get blocked before the request even reaches the app.

`curl_cffi` fixes that: it does the TLS handshake the way Chrome/Safari/Firefox
do, so the request looks like it came from a real browser.

- `main.py` - sends the same request as a plain client, then as Chrome, Safari
  and Firefox, and prints each JA3. The plain one is different; the impersonated
  ones match a real browser.
- `client.py` - a small session wrapper: keeps the impersonated fingerprint,
  takes an optional proxy, retries on 5xx/network errors.

## Run

```
pip install -r requirements.txt
python main.py
```

You'll see the JA3 of a plain client differ from the browser ones:

```
no impersonate   <some hash>
chrome           <chrome's hash>
safari           <safari's hash>
firefox          <firefox's hash>
```

## Using it

```python
from client import Client

c = Client(impersonate="chrome", proxy="http://user:pass@host:port")
r = c.get("https://example.com/api/items")
print(r.status_code, r.json())
```

## Notes

- `main.py` hits tls.peet.ws, a public TLS inspector, just to show the
  fingerprints. Everything else works against whatever target you point it at.
- Impersonation gets you past the TLS check; it isn't a license to ignore a
  site's terms or rate limits.
