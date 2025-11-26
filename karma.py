import time
import hashlib

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# 3 Weeks in seconds (3 * 7 * 24 * 60 * 60)
BAN_LEVEL_1_DURATION = 1814400 
# 6 Weeks in seconds
BAN_LEVEL_2_DURATION = 3628800 

# ---------------------------------------------------------
# 1. THE HASHER (Privacy First)
# ---------------------------------------------------------
def generate_hash_identity(user_data_string):
    """
    Turns "john@gmail.com" or "IP:192.168.1.1" into "8d9s8f9..."
    We observe the HASH, not the PERSON.
    """
    return hashlib.sha256(user_data_string.encode()).hexdigest()

# ---------------------------------------------------------
# 2. THE JUDGE (Your Logic)
# ---------------------------------------------------------
def assess_user_karma(user_history, new_rating):
    """
    Decides if a rating should be accepted, blocked, or 'flipped'.
    
    user_history: dict containing:
      - 'strikes': number of times they were flagged as 'petty'
      - 'last_ban_time': timestamp of when the last ban started
      - 'ratings_given': list of previous ratings [1, 1, 1, 5]
    
    new_rating: int (1-5)
    """
    now = time.time()
    strikes = user_history.get('strikes', 0)
    last_ban = user_history.get('last_ban_time', 0)
    
    # --- CHECK ACTIVE BANS ---
    
    # Level 1 Ban (3 Weeks)
    if strikes == 1:
        if (now - last_ban) < BAN_LEVEL_1_DURATION:
            return {
                "status": "blocked", 
                "reason": "Shadowban Level 1 (Active)",
                "final_score": None
            }
            
    # Level 2 Ban (6 Weeks)
    if strikes == 2:
        if (now - last_ban) < BAN_LEVEL_2_DURATION:
            return {
                "status": "blocked", 
                "reason": "Shadowban Level 2 (Active)",
                "final_score": None
            }

    # --- CHECK FOR "SKETCHY" PATTERNS ---
    # Example: If they try to give a 1-star, but their history shows they are toxic.
    is_toxic_behavior = False
    
    # Simple Heuristic: If they have given mostly 1-stars in the past
    previous_ratings = user_history.get('ratings_given', [])
    if len(previous_ratings) > 3:
        average_rating = sum(previous_ratings) / len(previous_ratings)
        if average_rating < 2.0 and new_rating == 1:
            is_toxic_behavior = True

    # --- APPLY JUDGMENT ---

    if strikes >= 3 or is_toxic_behavior:
        # THE JUDO FLIP (Your "1 jumps to 3" logic)
        final_score = new_rating
        
        if new_rating == 1:
            final_score = 3  # Neutralize the hate
            note = "Flipped 1 -> 3"
        elif new_rating == 3:
            final_score = 5  # Boost the apathy
            note = "Flipped 3 -> 5"
        else:
            note = "Score allowed"

        return {
            "status": "modified",
            "reason": f"Toxic Pattern Detected. {note}",
            "final_score": final_score
        }

    # If they are clean, accept the rating
    return {
        "status": "accepted",
        "reason": "Valid interaction",
        "final_score": new_rating
    }

# ---------------------------------------------------------
# TEST SCENARIO (For your own verification)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Let's test your "Sketchy" User
    bad_actor = {
        "strikes": 3,  # He is already on Strike 3
        "last_ban_time": time.time() - 10000, # Ban technically expired
        "ratings_given": [1, 1, 1, 2, 1] # He hates everything
    }

    # He tries to give a 1-star review to hurt a business
    verdict = assess_user_karma(bad_actor, new_rating=1)

    print(f"User Attempt: 1 Star")
    print(f"System Verdict: {verdict['status'].upper()}")
    print(f"Reason: {verdict['reason']}")
    print(f"Actual Rating Recorded: {verdict['final_score']} Stars")
