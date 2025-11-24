# fair-discovery-aggregator

[![Forever Free](https://img.shields.io/badge/Forever-Free-brightgreen)](https://github.com/)
[![Open Source](https://img.shields.io/badge/License-FDL%20v1.0-blue)](#license)
[![Founder](https://img.shields.io/badge/Founder-Jarrit%20Hosking-orange)](#founders-note)

Fair Discovery Aggregator — dual edition (frontend-only + optional hybrid backend)
A community-first, open, and free discovery protocol that ranks pages by human engagement.

## Contents

- `public/` — Frontend dashboard (GitHub Pages / Netlify friendly)
- `aggregator/` — Optional Python aggregator (server-side fetching)
- `functions/` — Firebase Cloud Functions (your provided code integrated)
- `LICENSE` — Fair Discovery License (FDL v1.0)
- `.gitignore`

## Quick start — Frontend (recommended, free)

1. Open `public/index.html`. Customize `public/sites.json` with seed discovery feeds.
2. Deploy the `public/` folder to GitHub Pages, Netlify, or any static host.
3. Visit the page and allow it to discover feeds automatically.

## Optional — Hybrid backend

If you want server-side caching and faster responses, use the `aggregator/` Python script or run the `functions/` Firebase code.

## Firebase setup (optional)

1. Install Firebase CLI and login: `npm install -g firebase-tools` then `firebase login`.
2. Initialize functions: `firebase init functions` (choose Node.js).
3. Copy the `functions/` folder into your Firebase project root.
4. Set environment variables for Gemini API as needed.
5. Deploy: `firebase deploy --only functions`

## Credits & Manifesto

## 🤝 The Fair Promise

Fair Discovery is, and will always be, **100% Free and Open Source**.

* **No Pay-to-Win:** You cannot buy a higher ranking. Rankings are based solely on real human engagement.
* **No Hidden Tracking:** We do not track users across the web.
* **No Gatekeeping:** The directory is open to everyone.

If you find value in this tool and want to support the server costs or the developer's caffeine intake, you can [Buy Me a Coffee](https://www.buymeacoffee.com/Prinymity). ☕

Founder: Jarrit Hosking
Manifesto: `FAIR_DISCOVERY_MANIFESTO.txt`

Medium article: https://medium.com/@jarrithosking/fair-web-discovery-30421c75bb3f

## License

This project is licensed under the **Fair Discovery License (FDL v1.0)** — see `LICENSE` for details.

## Founder's Note

Created by Jarrit Hosking — in the belief that fairness on the web should never be a luxury, but a right.
