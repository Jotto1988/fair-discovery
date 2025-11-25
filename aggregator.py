#!/usr/bin/env python3
import json
import requests
import time
import os
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
SITES_FILE = os.path.join(ROOT, "sites.json")
OUT_FILE = os.path.join(ROOT, "data.json")

# ---------------------------------------------------------
# CURATOR AI (Classification Logic)
# ---------------------------------------------------------
def ai_classify(domain, description, current_category):
    valid_cats = ["Auto", "Tech", "Health", "Retail", "Artists", "Service"]
    if current_category in valid_cats:
        return current_category

    text = (domain + " " + description).lower()
    vectors = {
        "Auto": ["panel", "motor", "car", "repair", "spray", "dent", "auto", "vehicle", "garage", "tires"],
        "Tech": ["soft", "app", "code", "data", "cyber", "web", "digital", "cloud", "bot", "ai"],
        "Health": ["med", "health", "care", "clinic", "doctor", "pharm", "skin", "dental", "wellness"],
        "Retail": ["shop", "store", "buy", "fashion", "gift", "sale", "mart", "boutique"],
        "Artists": ["art", "design", "music", "band", "paint", "studio", "creative", "photo", "gallery"]
    }

    best_cat = "Service"
    highest_score = 0

    for category, keywords in vectors.items():
        score = 0
        for word in keywords:
            if word in text:
                score += 1
        if score > highest_score:
            highest_score = score
            best_cat = category
    return best_cat

# ---------------------------------------------------------
# MAIN ENGINE
# ---------------------------------------------------------
def main():
    print("--- Fair Discovery Heavy-Duty Engine Starting ---")
    
    try:
        with open(SITES_FILE, "r") as f:
            data = json.load(f)
            sites = data.get("sites", [])
    except Exception as e:
        print(f"❌ Error loading sites.json: {e}")
        sites = []

    print(f"🔍 Scanning {len(sites)} network nodes...")
    merged_data = {}

    # Browser Headers to try and trick firewalls
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/json",
    }

    # 1. AUTOMATED SCANNING LOOP
    for feed_url in sites:
        print(f"\n👉 Connecting to: {feed_url}")
        try:
            # Verify=False ignores SSL errors
            response = requests.get(feed_url, headers=headers, timeout=20, verify=False)
            
            if response.status_code != 200: 
                print(f"   ⚠️ BLOCKED/ERROR: Status {response.status_code}")
                continue
            
            try:
                feed_json = response.json()
            except:
                print("   ⚠️ Content is not valid JSON.")
                continue

            # Parse Data
            parts = feed_url.split("/")
            origin = parts[0] + "//" + parts[2]
            domain = parts[2]

            raw_cat = feed_json.get("category", "Service")
            desc = feed_json.get("description", "")
            final_cat = ai_classify(domain, desc, raw_cat)
            
            pages = feed_json.get("pages", [])
            page_count = len(pages)
            print(f"   ✅ Success! Found {page_count} pages.")

            for page in pages:
                raw_url = page.get("url", "")
                score = int(page.get("score", 0))
                if not raw_url: continue

                if raw_url.startswith("http"): full_url = raw_url
                else: full_url = f"{origin}/{raw_url.lstrip('/')}"
                
                if full_url not in merged_data:
                    merged_data[full_url] = {
                        "url": full_url,
                        "score": 0,
                        "category": final_cat,
                        "description": desc,
                        "whatsapp": feed_json.get("whatsapp"),
                        "location": feed_json.get("location", "Global")
                    }
                merged_data[full_url]["score"] += score

        except Exception as e:
            print(f"   ❌ Connection Failed: {e}")
            continue

    # 2. PREPARE OUTPUT LIST
    output_list = list(merged_data.values())

    # ---------------------------------------------------------
    # 🛑 MANUAL OVERRIDE (BACKDOOR FOR BLOCKED SITES)
    # ---------------------------------------------------------
    # We manually inject Sky Rope here because Vehost blocks the robot.
    sky_rope_manual = {
        "url": "https://www.skyropespecialist.co.za/",
        "score": 100, # Placeholder score (You can update this manually later)
        "category": "Service",
        "description": "Professional rope access and high-altitude maintenance specialists.",
        "whatsapp": "27000000000", # PLEASE UPDATE THIS NUMBER IF NEEDED
        "location": "Cape Town, SA"
    }

    # Check if the robot found it automatically. If not, inject it.
    found_automatically = False
    for p in output_list:
        if "skyropespecialist.co.za" in p['url']:
            found_automatically = True
            break
    
    if not found_automatically:
        print("\n🔧 MANUAL INJECTION: Adding Sky Rope Specialist (Bypassing Firewall)")
        output_list.append(sky_rope_manual)
    # ---------------------------------------------------------

    # 3. FINAL SORT & SAVE
    output_list.sort(key=lambda x: x["score"], reverse=True)

    final_json = {
        "generated_at": int(time.time()),
        "node_count": len(sites),
        "pages": output_list
    }

    try:
        with open(OUT_FILE, "w") as f:
            json.dump(final_json, f, indent=2)
        print(f"\n💾 DATABASE SAVED: {len(output_list)} active listings.")
    except Exception as e:
        print(f"❌ Save Error: {e}")

if __name__ == "__main__":
    main()
