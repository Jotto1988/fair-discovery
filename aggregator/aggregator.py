#!/usr/bin/env python3
# Simple Python aggregator - fetches feeds listed in sites.json and outputs merged JSON.
import json, requests, time, os

ROOT = os.path.dirname(__file__)
SITES_FILE = os.path.join(ROOT, "sites.json")
OUT_FILE = os.path.join(ROOT, "data.json")

try:
    with open(SITES_FILE, "r") as f:
        s = json.load(f)
        sites = s.get("sites", [])
except Exception:
    sites = []

merged = {}
for feed in sites:
    try:
        r = requests.get(feed, timeout=5)
        if r.status_code != 200:
            continue
        js = r.json()
        origin = feed.split("/")[0] + "//" + feed.split("/")[2]
        for p in js.get("pages", []):
            url = p.get("url")
            score = int(p.get("score",0))
            if not url: continue
            if url.startswith("http"):
                key = url
            else:
                key = origin.rstrip("/") + "/" + url.lstrip("/")
            if key not in merged:
                merged[key] = {"url": key, "score": 0, "sites": set()}
            merged[key]["score"] += score
            merged[key]["sites"].add(origin)
    except Exception:
        continue

out = {"generated_at": int(time.time()), "count": len(merged), "pages": []}
for v in merged.values():
    v["sites"] = list(v["sites"])
    out["pages"].append(v)
out["pages"].sort(key=lambda x: x["score"], reverse=True)

with open(OUT_FILE, "w") as f:
    json.dump(out, f, indent=2)
print("Wrote", OUT_FILE)
