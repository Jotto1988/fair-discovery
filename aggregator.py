#!/usr/bin/env python3
import json
import requests
import time
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# We use absolute paths to ensure GitHub Actions finds the files 
# regardless of where the script is called from.
ROOT = os.path.dirname(os.path.abspath(__file__))
SITES_FILE = os.path.join(ROOT, "sites.json")
OUT_FILE = os.path.join(ROOT, "data.json")

def main():
    print("--- Fair Discovery Aggregator Starting ---")
    print(f"📂 Loading sites from: {SITES_FILE}")

    # 1. Load the list of sites to scan
    try:
        with open(SITES_FILE, "r") as f:
            data = json.load(f)
            sites = data.get("sites", [])
    except FileNotFoundError:
        print("❌ Error: sites.json not found.")
        sites = []
    except json.JSONDecodeError:
        print("❌ Error: sites.json is not valid JSON.")
        sites = []

    print(f"🔍 Found {len(sites)} feeds to scan.")

    merged_data = {}

    # 2. Loop through each site and fetch data
    for feed_url in sites:
        print(f"   👉 Scanning: {feed_url}...")
        
        try:
            # Set a timeout so the script doesn't hang on slow sites
            response = requests.get(feed_url, timeout=10)
            
            if response.status_code != 200:
                print(f"      ⚠️ Failed (Status {response.status_code})")
                continue
            
            feed_json = response.json()
            
            # Determine the 'Origin' (Domain) to fix relative URLs
            # Example: https://site.com/discovery.json -> https://site.com
            parts = feed_url.split("/")
            origin = parts[0] + "//" + parts[2]
            
            # Process the pages from this feed
            pages = feed_json.get("pages", [])
            for page in pages:
                raw_url = page.get("url", "")
                score = int(page.get("score", 0))
                
                if not raw_url:
                    continue

                # URL Normalization: Make sure all links are absolute
                if raw_url.startswith("http"):
                    full_url = raw_url
                else:
                    # Fix /page.html vs page.html
                    clean_segment = raw_url.lstrip("/")
                    full_url = f"{origin}/{clean_segment}"
                
                # Deduplication Logic
                # If two sites list the same URL, we sum their scores
                if full_url not in merged_data:
                    merged_data[full_url] = {
                        "url": full_url,
                        "score": 0,
                        "sources": [] # Track who listed this page
                    }
                
                merged_data[full_url]["score"] += score
                
                # Record the source (Origin) if not already listed
                if origin not in merged_data[full_url]["sources"]:
                    merged_data[full_url]["sources"].append(origin)

        except Exception as e:
            print(f"      ❌ Error processing feed: {e}")
            continue

    # 3. Format the output for the Search Engine
    output_list = []
    for key, value in merged_data.items():
        output_list.append(value)

    # 🤖 AI SORTING: Sort by Engagement Score (Highest First)
    # This ensures the "best" content appears at the top of the directory.
    output_list.sort(key=lambda x: x["score"], reverse=True)

    final_json = {
        "generated_at": int(time.time()),
        "total_sites_scanned": len(sites),
        "total_pages_indexed": len(output_list),
        "pages": output_list
    }

    # 4. Save to data.json
    try:
        with open(OUT_FILE, "w") as f:
            json.dump(final_json, f, indent=2)
        print(f"✅ Success! Database updated with {len(output_list)} pages.")
        print(f"💾 Saved to: {OUT_FILE}")
    except Exception as e:
        print(f"❌ Error writing output file: {e}")

if __name__ == "__main__":
    main()
