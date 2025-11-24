# Fair Discovery Engine 🌍

A lightweight, privacy-focused website analytics tool that prevents ad fraud by only triggering tracking pixels when real human engagement is detected.

## Why use this?
1. **Stop Bot Fraud:** The "Smart Pixel" logic ensures Facebook/Google pixels only fire if the user scrolls or interacts. Bots that bounce immediately cost you nothing.
2. **Accurate Data:** Tracks unique weekly visitors without complex cookies or databases.
3. **No Database Required:** Runs entirely on a simple JSON file and PHP script.

## Installation

1. Upload the `fair-discovery` folder to your website root (e.g., `public_html/fair-discovery`).
2. Edit `engagement.js` and add your **Facebook Pixel ID**.
3. Add this script to your website footer (before `</body>`):
   ```html
   <script src="/fair-discovery/engagement.js"></script>