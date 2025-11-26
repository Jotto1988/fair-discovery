#!/usr/bin/env python3
import json
import requests
import time
import os
import urllib3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(ROOT, "data.json")

# --- AI CLASSIFIER ---
def ai_classify(domain, description, current_category):
    valid_cats = ["Auto", "Tech", "Health", "Retail", "Artists", "Service", "Real Estate", "Travel"]
    if current_category in valid_cats: return current_category
    text = (str(domain) + " " + str(description)).lower()
    vectors = {
        "Auto": ["panel", "motor", "car", "repair", "spray", "dent", "mechanic", "parts", "glass"],
        "Tech": ["soft", "app", "code", "data", "cyber", "web", "digital", "bot", "ai"],
        "Health": ["med", "health", "care", "clinic", "doctor", "pharm", "dental"],
        "Retail": ["shop", "store", "buy", "fashion", "gift", "sale", "mart"],
        "Artists": ["art", "design", "music", "band", "paint", "studio", "photo"],
        "Real Estate": ["property", "estate", "realtor", "home", "house", "rent"],
        "Travel": ["travel", "tour", "trip", "holiday", "hotel", "flight"]
    }
    best_cat = "Service"
    highest_score = 0
    for category, keywords in vectors.items():
        score = sum(1 for word in keywords if word in text)
        if score > highest_score:
            highest_score = score
            best_cat = category
    return best_cat

def main():
    print("--- Fair Discovery Portal-First Engine ---")
    
    merged_data = {}
    
    # 1. CONNECT TO FIREBASE (THE TRUTH)
    try:
        key_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        if not key_json:
            print("❌ STOP: No FIREBASE_SERVICE_ACCOUNT secret found.")
            return

        cred_dict = json.loads(key_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("🔥 Connected to Database.")
        
        # 2. DOWNLOAD ALL PROFILES
        docs = db.collection('businesses').stream()
        
        # Headers for verification attempt
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
        }

        for doc in docs:
            data = doc.to_dict()
            
            # Basic validation: Must have at least a name/site
            if not data.get('site'): continue
            
            # Prepare the Entry based on PORTAL DATA (Guaranteed Listing)
            url = data.get('site', '')
            if url and not url.startswith('http'): url = 'https://' + url
            
            # Clean domain for ID
            try:
                domain = url.split("//")[1].split("/")[0]
            except:
                domain = url

            entry = {
                "url": url,
                "score": 10, # Base score for just existing
                "category": data.get('category', 'Service'),
                "description": data.get('description', ''),
                "location": data.get('location', 'Global'),
                "whatsapp": data.get('whatsapp', ''),
                "logo": data.get('logo', ''),
                "email": data.get('email', ''),
                "telephone": data.get('telephone', ''),
                "verified_tech": False 
            }

            # 3. ATTEMPT VERIFICATION (The "Nice to have")
            # If this fails due to firewall, WE DO NOT DELETE. We just don't give the bonus points.
            verify_url = f"{url.rstrip('/')}/fair-discovery/discovery.json"
            print(f"👉 Processing: {domain} ...", end=" ")
            
            try:
                response = requests.get(verify_url, headers=headers, timeout=5, verify=False)
                if response.status_code == 200:
                    # It worked! They are verified.
                    # We can even update data with the file if we want, or stick to Portal data.
                    # Let's verify category via AI here
                    entry["category"] = ai_classify(domain, entry["description"], entry["category"])
                    entry["score"] = 100 # BOOM! Verified Score.
                    entry["verified_tech"] = True
                    print("✅ Verified (100 Auth)")
                else:
                    print(f"⚠️ Unverified (Status {response.status_code}) - Keeping Listing")
            except:
                print("❌ Firewall/Offline - Keeping Listing")

            # Add to master list
            merged_data[url] = entry

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return

    # 4. SAVE
    output_list = list(merged_data.values())
    output_list.sort(key=lambda x: x["score"], reverse=True)
    
    final_json = {
        "generated_at": int(time.time()),
        "node_count": len(output_list),
        "pages": output_list
    }

    with open(OUT_FILE, "w") as f:
        json.dump(final_json, f, indent=2)
    print(f"\n💾 DATABASE SAVED: {len(output_list)} listings.")

if __name__ == "__main__":
    main()
