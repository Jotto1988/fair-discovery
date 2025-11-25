# Fair Discovery Engine 🌍

**The decentralized, human-first website directory.** Fair Discovery ranks websites based on *verified human interaction*, blocking bots to reveal true authority. This forces ad networks to deliver real traffic, protecting your budget.

---

## 🚀 How to Join (3 Simple Steps)

### Step 1: Download the Kit
1.  Go to the **[public folder](https://github.com/fair-collective/fair-discovery/tree/main/public)** in this repository.
2.  Download the contents (or the whole zip).
3.  You need 3 specific files: `engagement.js`, `record.php`, and `discovery.json`.

### Step 2: Install on your Website
1.  Create a folder named `fair-discovery` in your website's root (public_html).
2.  Upload the 3 files into that folder.
3.  Add this script line to your website's **Footer** (before the closing `</body>` tag):
    ```html
    <script src="/fair-discovery/engagement.js"></script>
    ```
4.  **(Optional)** To see your own stats, upload the `dashboard_template.html` as `index.html` inside that folder.

### Step 3: Join the Network
1.  Go to our **[Issues Page](https://github.com/fair-collective/fair-discovery/issues/new?title=Add%20Site%3A%20[YOUR_URL_HERE]&body=Please%20add%20my%20feed:%20https://your-site.com/fair-discovery/discovery.json)**.
2.  Paste your discovery link (e.g., `https://yoursite.com/fair-discovery/discovery.json`).
3.  Submit the issue. Our robot will verify your site and add you to the search engine automatically!

---

## ⚙️ Configuration (discovery.json)

To get a **Premium Card** listing with your logo flag, category, and description, format your `discovery.json` like this:

```json
{
  "site": "your-website.com",
  "category": "Tech", 
  "description": "A short, punchy summary of what you do (Max 140 chars).",
  "whatsapp": "27820000000",
  "location": "Cape Town, SA",
  "visitors": {
    "current_week_start": "2025-01-01",
    "week_1": 0, "week_2": 0, "week_3": 0, "week_4": 0
  },
  "pages": []
}
