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

## Hosting

Served free with GitHub Pages at **forge2forge.com** once the domain is pointed here.
