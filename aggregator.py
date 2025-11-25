# ---------------------------------------------------------
    # 🛑 MANUAL OVERRIDES (BACKDOOR INJECTIONS)
    # ---------------------------------------------------------
    
    # 1. IntPanelShop (Added to safety net)
    intpanel = {
        "url": "https://www.intpanelshop.co.za/",
        "score": 66100000,  # Based on your last screenshot
        "category": "Auto",
        "description": "Expert panel beating and spray painting in Cape Town.",
        "whatsapp": "27821234567", 
        "location": "Cape Town, SA"
    }

    # 2. Sky Rope Specialist
    sky_rope = {
        "url": "https://www.skyropespecialist.co.za/",
        "score": 2200, 
        "category": "Service",
        "description": "Professional rope access and high-altitude maintenance specialists.",
        "whatsapp": "27000000000",
        "location": "Cape Town, SA"
    }

    # 3. Jotto's Portfolio
    jotto_portfolio = {
        "url": "https://jotto1988.github.io/jotto.github.io/",
        "score": 500, 
        "category": "Tech",
        "description": "Jotto's Portfolio: Open Source projects, Fair Discovery development, and AI innovations.",
        "whatsapp": "",
        "location": "Global"
    }

    # 4. Seriti PBO
    seriti = {
        "url": "https://www.seritipbo.org/",
        "score": 150, 
        "category": "Service",
        "description": "Public Benefit Organization (PBO) dedicated to community upliftment and social welfare.",
        "whatsapp": "", 
        "location": "South Africa"
    }

    # 5. Bookkeepers in Cape Town
    bookkeeper = {
        "url": "https://bookkeepersincapetown.co.za/",
        "score": 150, 
        "category": "Service",
        "description": "Professional bookkeeping and accounting services for businesses in South Africa and the UK.",
        "whatsapp": "27000000000", 
        "location": "Cape Town, SA"
    }

    # Inject if missing
    current_urls = [p['url'] for p in output_list]
    
    if intpanel['url'] not in current_urls:
        print("\n🔧 MANUAL: Restoring IntPanelShop")
        output_list.append(intpanel)

    if sky_rope['url'] not in current_urls:
        output_list.append(sky_rope)

    if jotto_portfolio['url'] not in current_urls:
        output_list.append(jotto_portfolio)

    if seriti['url'] not in current_urls:
        output_list.append(seriti)

    if bookkeeper['url'] not in current_urls:
        output_list.append(bookkeeper)
        
    # ---------------------------------------------------------
