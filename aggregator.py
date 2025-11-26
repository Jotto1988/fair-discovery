#!/usr/bin/env python3
import json
import requests
import time
import os
import urllib3

# Disable SSL warnings for strict firewalls
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
        "Auto": ["panel", "motor", "car", "repair", "spray", "dent", "auto", "vehicle", "garage", "tires", "mechanic", "parts"],
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

    # Headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/json",
    }

    # 1. AUTOMATED SCANNING LOOP
    for feed_url in sites:
        print(f"\n👉 Connecting to: {feed_url}")
        try:
            response = requests.get(feed_url, headers=headers, timeout=20, verify=False)
            
            if response.status_code != 200: 
                print(f"   ⚠️ BLOCKED/ERROR: Status {response.status_code}")
                continue
            
            try:
                feed_json = response.json()
            except:
                print("   ⚠️ Content is not valid JSON.")
                continue

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
    # 🛑 MANUAL OVERRIDES (SAFETY NET)
    # ---------------------------------------------------------
    
    # 1. IntPanelShop
    intpanel = { "url": "https://www.intpanelshop.co.za/", "score": 66100000, "category": "Auto", "description": "Expert panel beating and spray painting in Cape Town.", "whatsapp": "27821234567", "location": "Cape Town, SA" }
    
    # 2. Sky Rope Specialist
    sky_rope = { "url": "https://www.skyropespecialist.co.za/", "score": 2200, "category": "Service", "description": "Professional rope access and high-altitude maintenance specialists.", "whatsapp": "27000000000", "location": "Cape Town, SA" }
    
    # 3. Jotto's Portfolio
    jotto_portfolio = { "url": "https://jotto1988.github.io/jotto.github.io/", "score": 500, "category": "Tech", "description": "Jotto's Portfolio: Open Source projects, Fair Discovery development, and AI innovations.", "whatsapp": "", "location": "Global" }
    
    # 4. Seriti PBO
    seriti = { "url": "https://www.seritipbo.org/", "score": 150, "category": "Service", "description": "Non-profit organization providing skill development training in plumbing and community upliftment.", "whatsapp": "", "location": "South Africa" }
    
    # 5. Bookkeepers in Cape Town
    bookkeeper = { "url": "https://bookkeepersincapetown.co.za/", "score": 150, "category": "Service", "description": "Professional bookkeeping and accounting services for businesses in South Africa and the UK.", "whatsapp": "27000000000", "location": "Cape Town, SA" }
    
    # 6. Grey Zone Auto Parts (WhatsApp is the site - Placeholder URL)
    grey_zone = { 
        "url": "https://greyzoneautoparts.local", 
        "score": 150, 
        "category": "Auto", 
        "description": "Automotive parts sales based in Pretoria, delivering nationwide.", 
        "whatsapp": "27817985689", # WhatsApp is the destination
        "location": "Pretoria, SA" 
    }

    # 7. AO Locksmith (WhatsApp is the site - Placeholder URL)
    ao_locksmith = { 
        "url": "https://aolocksmith.local", 
        "score": 150, 
        "category": "Service", 
        "description": "Specialist car locksmith. Cutting, coding, and programming car keys.", 
        "whatsapp": "27812099604", # WhatsApp is the destination
        "location": "Pretoria, SA" 
    }
    
    # 8. Auto Digital Solutions (AutoDS)
    mobile_mechanic = { "url": "https://autods.co.za/", "score": 150, "category": "Auto", "description": "Top-rated mobile mechanic in Cape Town. We come to you.", "whatsapp": "27000000000", "location": "Cape Town, SA" }
    
    # 9. Save Our Children (Scouts)
    scouts = { "url": "https://scoutsforkids.org/", "score": 150, "category": "Service", "description": "Non-profit offering hiking, education, and community engagement to keep kids safe from drugs and violence.", "whatsapp": "27717990196", "location": "Cape Town, SA" }

    # Injection Logic
    current_urls = [p['url'] for p in output_list]
    
    if intpanel['url'] not in current_urls: output_list.append(intpanel)
    if sky_rope['url'] not in current_urls: output_list.append(sky_rope)
    if jotto_portfolio['url'] not in current_urls: output_list.append(jotto_portfolio)
    if seriti['url'] not in current_urls: output_list.append(seriti)
    if bookkeeper['url'] not in current_urls: output_list.append(bookkeeper)
    if grey_zone['url'] not in current_urls: output_list.append(grey_zone)
    if ao_locksmith['url'] not in current_urls: output_list.append(ao_locksmith)
    if mobile_mechanic['url'] not in current_urls: output_list.append(mobile_mechanic)
    if scouts['url'] not in current_urls: output_list.append(scouts)
        
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
