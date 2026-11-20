# Forge2Forge Website

The website for **Forge2Forge**, the podcast with Jeff Needham and Tyler Jones.
We sit down with men to talk about the forges of life God has taken them through.

- YouTube: https://www.youtube.com/@forge2forge
- TikTok: https://www.tiktok.com/@forge2forge
- Email: coupleofmessedupguys@forge2forge.com

## What's in here

| File | What it is |
|---|---|
| `index.html` | The whole website (page, styles, images and scripts in one file) |
| `forge-bg.mp4` | The forge video that plays behind the site |
| `forge-bg-poster.jpg` | Still frame shown on phones instead of the video |
| `manifest.webmanifest` | Lets people install the site as an app on iPhone and Android |
| `sw.js` | Keeps the app loading fast and working on a weak connection |
| `icons/` | App icons and browser tab icon (the Forge2Forge shield) |
| `.nojekyll` | Tells GitHub Pages to serve the files exactly as they are |

## Adding resources

Open `index.html`, search for `RESOURCES LIST`, and add a line like:

```js
{ name: "Ministry name", url: "https://example.org", category: "Recovery", desc: "One or two sentences." },
```

## Notifications

People tap **Get Notified** on the site (on iPhone, inside the installed app) to get a push notification
when a new full episode posts on YouTube or a new resource is added. It runs through OneSignal
(app ID `f7331118-8204-445b-9878-9396bafcc735`).

- `.github/workflows/notify.yml` checks YouTube every hour, and runs right away when `index.html` changes.
- `notify/notify.py` does the checking and sending. `notify/state.json` remembers what was already announced.
- The OneSignal API key is the GitHub secret `ONESIGNAL_API_KEY`.
- To send a test: **Actions** tab → **Notifications** → **Run workflow** → choose `test`.

## Hosting

Served free with GitHub Pages at **forge2forge.com** once the domain is pointed here.
