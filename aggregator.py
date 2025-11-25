#!/usr/bin/env python3
import json
import requests
import time
import os

# ---------------------------------------------------------
# ⚙️ CONFIGURATION
# ---------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
SITES_FILE = os.path.join(ROOT, "sites.json")
OUT_FILE = os.path.join(ROOT, "data.json")

# ---------------------------------------------------------
# 🧠 CURATOR AI: Semantic Classifier (Expert System)
# ---------------------------------------------------------
def ai_classify(domain, description, current_category):
    """
    Analyzes domain text and description to autonomously assign 
    the most accurate category if the user provided a generic one.
    """
    # 1. Trust the Human (Human-in-the-loop)
    # If they selected a specific category, respect it.
    valid_cats = ["Auto", "Tech", "Health", "Retail", "Artists"]
    if current_category in valid_cats:
        return current_category

    # 2. Prepare Data for Analysis
    # Combine domain and description into a single semantic vector
    text = (domain + " " + description).lower()
    
    # 3. Knowledge Base (Weighted Vectors)
    vectors = {
        "Auto": ["panel", "motor", "car", "repair", "spray", "dent", "auto", "vehicle", "garage", "tires", "wheels"],
        "Tech": ["soft", "app", "code", "data", "cyber", "web", "digital", "cloud", "bot", "ai", "compute", "network"],
        "Health": ["med", "health", "care", "clinic", "doctor", "pharm", "skin", "dental", "wellness", "therapy"],
        "Retail": ["shop", "store", "buy", "fashion", "gift", "sale", "mart", "boutique", "market"],
        "Artists": ["art", "design", "music", "band", "paint", "studio", "creative", "photo", "gallery", "ink"]
    }

    # 4. Inference Engine
    best_cat = "Service" # Default fallback
    highest_score = 0

    for category, keywords in vectors.items():
        score = 0
        for word in keywords:
            if word in text:
                score += 1
        
        # If we find a stronger match, update our hypothesis
        if score > highest_score:
            highest_score = score
            best_cat = category
            
    return best_cat

# ---------------------------------------------------------
# 🚀 MAIN ENGINE
# ---------------------------------------------------------
def main():
    print("--- Fair Discovery Dual-AI Engine Starting ---")
    
    # 1. Load Network Nodes
    try:
        with open(SITES_FILE, "r") as f:
            data = json.load(f)
            sites = data.get("sites", [])
    except Exception as e:
        print(f"❌ Error loading sites: {e}")
        sites = []

    print(f"🔍 Scanning {len(sites)} network nodes...")
    merged_data = {}

    # 2. Traverse the Network
    for feed_url in sites:
        try:
            # Fetch the JSON from the remote node
            response = requests.get(feed_url, timeout=10)
            if response.status_code != 200: 
                print(f"   ⚠️ Unreachable: {feed_url}")
                continue
            
            feed_json = response.json()
            
            # Parse Origin (Domain)
            parts = feed_url.split("/")
            origin = parts[0] + "//" + parts[2]
            domain = parts[2]

            # Extract Raw Metadata
            raw_cat = feed_json.get("category", "Service")
            desc = feed_json.get("description", "")
            
            # 🤖 EXECUTE CURATOR AI
            # The AI decides the final category based on context
            final_cat = ai_classify(domain, desc, raw_cat)
            
            # Process & Aggregate Pages
            pages = feed_json.get("pages", [])
            for page in pages:
                raw_url = page.get("url", "")
                # The Score here comes from the Edge AI (Behavioral)
                score = int(page.get("score", 0))
                
                if not raw_url: continue

                # URL Normalization
                if raw_url.startswith("http"): full_url = raw_url
                else: full_url = f"{origin}/{raw_url.lstrip('/')}"
                
                # Database Construction
                if full_url not in merged_data:
                    merged_data[full_url] = {
                        "url": full_url,
                        "score": 0,
                        "category": final_cat,  # Assigned by Curator AI
                        "description": desc,
                        "whatsapp": feed_json.get("whatsapp"),
                        "location": feed_json.get("location", "Global")
                    }
                
                # Accumulate Authority Score
                merged_data[full_url]["score"] += score

        except Exception as e:
            print(f"   ⚠️ Node Error {feed_url}: {e}")
            continue

    # 3. Final Sort (Authority Ranking)
    # This ranks based on the Edge AI's findings
    output_list = list(merged_data.values())
    output_list.sort(key=lambda x: x["score"], reverse=True)

    final_json = {
        "generated_at": int(time.time()),
        "node_count": len(sites),
        "system_version": "Fair-Discovery-v3.2",
        "ai_modules": ["Edge-Behavioral", "Curator-Semantic"],
        "pages": output_list
    }

    # 4. Publish Database
    try:
        with open(OUT_FILE, "w") as f:
            json.dump(final_json, f, indent=2)
        print(f"✅ Success! Database updated with {len(output_list)} listings.")
        print("   Edge AI data integrated.")
        print("   Curator AI classification complete.")
    except Exception as e:
        print(f"❌ Save Error: {e}")

if __name__ == "__main__":
    main()
