# Forge2Forge Brand Kit

Everything here matches the website at forge2forge.com. Use these files for any new graphics so the look stays the same.

## The rules
- **Lettering:** hammered fiery gold, raised 3D. "FORGE" is gold, never white.
- **The 2:** the shape of the hand-made 2 from the sign, finished in forged gold with a chiseled edge. Whenever "Forge2Forge" is written out as a title, use the big gold `forge2forge-2.png` from the sign between the two "FORGE"s (see `forge2forge-wordmark.png`). Never a typed "2".
- **Glow:** white fading to light blue, behind the shield only (not the swords), like the studio sign's backlight.
- **Background:** dark forge, with an orange ember glow and floating sparks.
- **Tagline:** "Just a couple of messed-up guys, livin' in a messed-up world, talkin' about how we do it all for the glory of God."

## Files
| File | Use it for |
|---|---|
| `forge2forge-logo.png` | The shield logo, clear background: the studio sign with forged gold 3D lettering and 2 |
| `forge2forge-logo-glow.png` | Shield with the white-to-blue glow |
| `forge2forge-wordmark.png` | "FORGE 2 FORGE" title in gold, clear background |
| `forge2forge-2.png` | The gold 2 by itself |
| `youtube-banner-2560x1440.png` | YouTube channel banner (key content inside the 1546 x 423 center) |
| `facebook-cover-1640x624.png` | Facebook cover photo |
| `profile-picture-1000x1000.png` | YouTube, Facebook and TikTok profile picture (ember background) |
| `profile-picture-black-1000x1000.png` | Same, on pure black |
| `youtube-watermark-300x300.png` | YouTube video watermark |
| `shield-J.png`, `shield-T.png`, `shield-blank.png` | Host shields (Jeff, Tyler) and a blank shield |
| `forge2forge-qr.png` | QR code to forge2forge.com, for printing |
| `link-preview-card-1200x630.jpg` | The card that shows when the site link is shared |
| `sign-photo-original.png` | Original photo of the sign (epoxy letters) |
| `sign-photo-glare-free.png` | The sign photo, cut out, before the lettering was redone |
| `logo-lettering-comparison.jpg` | The sign photo next to the finished logo |

## Rebuilding
The website's source and tools live in `../source`:
- `source/template.html` is the website; `python3 source/build.py` rebuilds `index.html` and `version.json`.
- `source/make_banners.py` makes the YouTube and Facebook banners.
