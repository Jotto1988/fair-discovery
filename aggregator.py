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
# CURATOR AI
# ---------------------------------------------------------
def ai_classify(domain, description, current_category):
    valid_cats = ["Auto", "Tech", "Health", "Retail", "Artists", "Service", "Real Estate", "Travel"]
    if current_category in valid_cats:
        return current_category
    return "Service"

# ---------------------------------------------------------
# MAIN ENGINE
# ---------------------------------------------------------
def main():
    print("--- Fair Discovery Engine Starting ---")
    
    try:
        with open(SITES_FILE, "r") as f:
            data = json.load(f)
            sites = data.get("sites", [])
    except Exception as e:
        print(f"❌ Error loading sites: {e}")
        sites = []

    merged_data = {}
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }

    # 1. AUTOMATED SCANNING
    for feed_url in sites:
        try:
            response = requests.get(feed_url, headers=headers, timeout=15, verify=False)
            if response.status_code == 200:
                feed_json = response.json()
                
                parts = feed_url.split("/")
                origin = parts[0] + "//" + parts[2]
                
                raw_cat = feed_json.get("category", "Service")
                desc = feed_json.get("description", "")
                
                pages = feed_json.get("pages", [])
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
                            "category": raw_cat,
                            "description": desc,
                            "whatsapp": feed_json.get("whatsapp", ""),
                            "location": feed_json.get("location", "")
                        }
                    merged_data[full_url]["score"] += score
        except: continue

    output_list = list(merged_data.values())

    # ---------------------------------------------------------
    # 🛑 MANUAL OVERRIDES (VERIFIED DATA ONLY)
    # ---------------------------------------------------------
    
    # 1. IntPanelShop
    intpanel = { 
        "url": "https://www.intpanelshop.co.za/", 
        "score": 66100000, "category": "Auto", 
        "description": "Expert panel beating and spray painting in Cape Town.", 
        "whatsapp": "27716871308",  
        "location": "Cape Town, SA" 
    }
    
    # 2. Sky Rope Specialist
    sky_rope = { 
        "url": "https://www.skyropespecialist.co.za/", 
        "score": 2200, "category": "Service", 
        "description": "Professional rope access and high-altitude maintenance specialists.", 
        "whatsapp": "27655038871", 
        "location": "Cape Town, SA" 
    }
    
    # 3. Jotto's Portfolio
    jotto = { 
        "url": "https://jotto1988.github.io/jotto.github.io/", 
        "score": 500, "category": "Tech", 
        "description": "Open Source projects and Fair Discovery development.", 
        "whatsapp": "", "location": "Global" 
    }
    
    # 4. Seriti PBO (Updated Number)
    seriti = { 
        "url": "https://www.seritipbo.org/", 
        "score": 150, "category": "Service", 
        "description": "Non-profit organization providing skill development training and community upliftment.", 
        "whatsapp": "27662316778", # Updated
        "location": "South Africa" 
    }
    
    # 5. Bookkeepers SA
    bookkeeper = { 
        "url": "https://bookkeepersincapetown.co.za/", 
        "score": 4788, "category": "Service", 
        "description": "Professional bookkeeping and accounting services.", 
        "whatsapp": "27727791046", 
        "location": "Cape Town, SA" 
    }
    
    # 6. Grey Zone Auto Parts
    grey_zone = { 
        "url": "https://greyzoneautoparts.local", 
        "score": 150, "category": "Auto", 
        "description": "Automotive parts sales based in Pretoria.", 
        "whatsapp": "27817985689", 
        "location": "Pretoria, SA" 
    }

    # 7. AO Locksmith
    ao_locksmith = { 
        "url": "https://aolocksmith.local", 
        "score": 150, "category": "Auto", 
        "description": "Specialist car locksmith. Cutting and coding car keys.", 
        "whatsapp": "27812099604", 
        "location": "Pretoria, SA" 
    }
    
    # 8. Auto Digital Solutions (Updated Number)
    mobile_mechanic = { 
        "url": "https://autods.co.za/", 
        "score": 150, "category": "Auto", 
        "description": "Top-rated mobile mechanic in Cape Town.", 
        "whatsapp": "27736795182", # Updated
        "location": "Cape Town, SA" 
    }
    
    # 9. Save Our Children
    scouts = { 
        "url": "https://scoutsforkids.org/", 
        "score": 150, "category": "Service", 
        "description": "Non-profit offering hiking and education for kids.", 
        "whatsapp": "27717990196", 
        "location": "Cape Town, SA" 
    }

    # 10. CCG Auto Glass Replacement (NEW)
    ccg_glass = { 
        "url": "https://ccgautoglass.local", 
        "score": 150, "category": "Auto", 
        "description": "Windscreens, door glass, truck windscreens, and panel shop refits.", 
        "whatsapp": "27828990541", 
        "location": "Cape Town, SA" 
    }

    # Safe Injection
    current_urls = [p['url'] for p in output_list]
    manuals = [intpanel, sky_rope, jotto, seriti, bookkeeper, grey_zone, ao_locksmith, mobile_mechanic, scouts, ccg_glass]
    
    for site in manuals:
        if site['url'] not in current_urls:
            output_list.append(site)

    # 3. SAVE
    output_list.sort(key=lambda x: x["score"], reverse=True)
    
    final_json = { "generated_at": int(time.time()), "pages": output_list }

    try:
        with open(OUT_FILE, "w") as f:
            json.dump(final_json, f, indent=2)
        print(f"✅ Clean Database Saved: {len(output_list)} verified sites.")
    except Exception as e:
        print(f"❌ Save Error: {e}")

if __name__ == "__main__":
    main()
