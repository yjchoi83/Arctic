import hashlib, json, os, sys, time, urllib.request, urllib.parse, urllib.error
BASE = "/d/yj_projects/workspace_yj/Arctic/arctic_explore"
CACHE = os.path.join(BASE, "scratch/s2cache")
os.makedirs(CACHE, exist_ok=True)
UA = "ArcticRefCheck/1.0 (mailto:ldg810@koreatech.ac.kr)"


def get(url, ratelimit=0.0):
    h = hashlib.sha1(url.encode()).hexdigest()
    p = os.path.join(CACHE, h + ".json")
    if os.path.exists(p):
        return json.load(open(p)).get("body")
    delays = [2, 4, 8]
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=45) as r:
                b = r.read().decode("utf-8", "replace")
            json.dump({"url": url, "body": b}, open(p, "w"))
            if ratelimit:
                time.sleep(ratelimit)
            return b
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < 3:
                time.sleep(delays[i])
                continue
            return json.dumps({"__error__": e.code, "url": url})
        except Exception as e:
            if i < 3:
                time.sleep(delays[i])
                continue
            return json.dumps({"__error__": str(e), "url": url})
    return None


def _year(m):
    for k in ("published-print", "published-online", "issued", "created"):
        if k in m:
            dp = m[k].get("date-parts", [[None]])
            if dp and dp[0] and dp[0][0]:
                return dp[0][0]
    return None


def cr_summary(doi):
    b = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    try:
        m = json.loads(b)["message"]
    except Exception:
        return None
    names = [(a.get("family", "") + " " + a.get("given", "")).strip() or a.get("name", "") for a in m.get("author", [])]
    return {"doi": m.get("DOI"), "title": (m.get("title") or [""])[0], "year": _year(m),
            "venue": (m.get("container-title") or [""])[0], "authors": names, "type": m.get("type"),
            "publisher": m.get("publisher", "")}


def cr_search(q, rows=5):
    b = get("https://api.crossref.org/works?rows=%d&query.bibliographic=%s" % (rows, urllib.parse.quote(q)))
    try:
        items = json.loads(b)["message"]["items"]
    except Exception:
        return []
    out = []
    for m in items:
        out.append({"doi": m.get("DOI"), "title": (m.get("title") or [""])[0], "year": _year(m),
                    "venue": (m.get("container-title") or [""])[0],
                    "authors": [a.get("family", "") for a in m.get("author", [])][:4], "type": m.get("type")})
    return out


def s2(q):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?limit=5&"
           "fields=title,year,venue,authors,externalIds&query=" + urllib.parse.quote(q))
    return get(url, ratelimit=1.2)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "search":
        for q in sys.argv[2:]:
            print("===", q)
            for r in cr_search(q, 6):
                print("   %s | %s | %s | %s | %s" % (r["year"], r["doi"], r["title"][:95], r["venue"][:45], r["authors"]))
    elif mode == "doi":
        for d in sys.argv[2:]:
            s = cr_summary(d)
            print(json.dumps(s, ensure_ascii=False))
    elif mode == "s2":
        for q in sys.argv[2:]:
            print("===", q)
            print(s2(q)[:1500])

