// The Forge2Forge app's one service worker. OneSignal requires this exact file name.
// It loads sw.js, which has the offline caching, notifications and the red number on the icon.
// build.py rewrites this file with a new version each time the site is rebuilt.
importScripts('/sw.js?v=20261124180146');
