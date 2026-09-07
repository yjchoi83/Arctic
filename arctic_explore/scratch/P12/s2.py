"""Semantic Scholar client: x-api-key header, <=1 req/s, exponential backoff."""
import json, os, time, urllib.parse, urllib.request, urllib.error, pathlib

KEY = os.environ.get("S2_API_KEY", "")
BASE = "https://api.semanticscholar.org/graph/v1"
CACHE = pathlib.Path(__file__).with_name("s2cache")
CACHE.mkdir(exist_ok=True)
_last = [0.0]


def _throttle():
    dt = time.time() - _last[0]
    if dt < 1.05:
        time.sleep(1.05 - dt)
    _last[0] = time.time()


def get(path, use_cache=True, **params):
    q = urllib.parse.urlencode(params)
    url = f"{BASE}{path}" + (f"?{q}" if q else "")
    ck = CACHE / (str(abs(hash(url))) + ".json")
    if use_cache and ck.exists():
        return json.loads(ck.read_text())
    delay = 3.0
    for attempt in range(7):
        _throttle()
        req = urllib.request.Request(url, headers={"x-api-key": KEY, "User-Agent": "arctic-p12/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.loads(r.read().decode())
            ck.write_text(json.dumps(out))
            return out
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 6:
                time.sleep(delay)
                delay = min(delay * 2, 90)
                continue
            return {"_error": f"HTTP {e.code}", "_url": url, "_body": e.read()[:300].decode("utf8", "replace")}
        except Exception as e:  # noqa: BLE001
            if attempt < 6:
                time.sleep(delay)
                delay = min(delay * 2, 90)
                continue
            return {"_error": repr(e), "_url": url}
    return {"_error": "exhausted", "_url": url}


def search(query, limit=20, fields="title,year,venue,externalIds,abstract,authors,citationCount"):
    return get("/paper/search", query=query, limit=limit, fields=fields)


if __name__ == "__main__":
    import sys
    r = search(sys.argv[1] if len(sys.argv) > 1 else "sea ice drift Sentinel-1", limit=3)
    print(json.dumps(r, indent=1)[:1500])
