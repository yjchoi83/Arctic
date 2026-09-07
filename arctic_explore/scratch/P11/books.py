import sys, json, urllib.parse
sys.path.insert(0, "/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/P11")
from fetch import get
for q in sys.argv[1:]:
    u = ("https://openlibrary.org/search.json?q=" + urllib.parse.quote(q) +
         "&fields=title,author_name,first_publish_year,publisher,isbn,number_of_pages_median&limit=4")
    print("===", q)
    try:
        d = json.loads(get(u))
    except Exception as e:
        print("  ERR", e); continue
    for doc in d.get("docs", []):
        isbn = (doc.get("isbn") or [])[:6]
        print("  %s | %s | %s | %s" % (doc.get("first_publish_year"), doc.get("title"),
              (doc.get("author_name") or [])[:3], (doc.get("publisher") or [])[:3]))
        print("     ISBN:", isbn)
