# Forge2Forge notifications: run by GitHub Actions (.github/workflows/notify.yml).
# Sends a push notification through OneSignal when a new full episode is on YouTube
# or a new resource is added to the RESOURCES LIST in index.html.
# What has already been announced is kept in notify/state.json.
# The first run only records what is there now, so nobody gets a pile of old alerts.
import json, os, re, sys, urllib.request, urllib.error, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STATE = os.path.join(ROOT, 'notify', 'state.json')
APP_ID = 'f7331118-8204-445b-9878-9396bafcc735'
UPLOADS = 'UUjbcS4FaIOdLdwyh8-4XMCA'
CLIP_SECONDS = 180          # same rule as the website: shorter videos are clips, not episodes
MAX_AGE_DAYS = 4            # never announce something older than this
SITE = 'https://forge2forge.com/'
ICON = SITE + 'icons/icon-192.png'


def get_json(url, headers=None, data=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def site_html():
    return open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()


def yt_key():
    k = os.environ.get('YT_API_KEY')
    if k:
        return k
    m = re.search(r"const KEY='(AIza[\w-]+)'", site_html())
    if not m:
        sys.exit('No YouTube API key found')
    return m.group(1)


def secs(d):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', d or '')
    return sum(int(x or 0) * f for x, f in zip(m.groups(), (3600, 60, 1))) if m else 0


def pretty(t):
    s = re.sub(r'\s*\|\s*Forge2Forge.*$', '', t, flags=re.I)
    s = re.sub(r'^\s*Forge2Forge\s*(Podcast)?\s*(Ep\.?\s*[_\d]*)?\s*[-|:]?\s*', '', s, flags=re.I)
    s = re.sub(r'^Ep\.?\s*[_\d]*\s*\|\s*', '', s, flags=re.I)
    s = ' '.join(w[0] + w[1:].lower() if re.fullmatch(r'[A-Z]{4,}', w) else w for w in s.split())
    return s.strip() or t


def episodes():
    """Newest public full episodes, newest first."""
    h = {'Referer': SITE}
    key = yt_key()
    p = get_json(f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=15&playlistId={UPLOADS}&key={key}', h)
    items = p.get('items', [])
    ids = ','.join(i['contentDetails']['videoId'] for i in items)
    if not ids:
        return []
    v = get_json(f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,status,snippet&id={ids}&key={key}', h)
    out = []
    for x in v.get('items', []):
        if x['status'].get('privacyStatus') != 'public':
            continue
        if x['snippet'].get('liveBroadcastContent', 'none') != 'none':   # upcoming premiere or live
            continue
        if secs(x['contentDetails'].get('duration')) <= CLIP_SECONDS:
            continue
        th = x['snippet'].get('thumbnails', {})
        thumb = (th.get('maxres') or th.get('high') or th.get('medium') or {}).get('url')
        out.append({'id': x['id'], 'title': pretty(x['snippet']['title']),
                    'date': x['snippet']['publishedAt'], 'thumb': thumb})
    out.sort(key=lambda e: e['date'], reverse=True)
    return out


def resources():
    """Names and descriptions from the RESOURCES LIST in index.html."""
    m = re.search(r'const RESOURCES = \[(.*?)\n\];', site_html(), re.S)
    if not m:
        return []
    return [{'name': n, 'desc': d} for n, d in
            re.findall(r'name:\s*"([^"]+)".*?desc:\s*"([^"]*)"', m.group(1), re.S)]


def send(heading, text, url, image=None):
    key = os.environ.get('ONESIGNAL_API_KEY')
    if not key:
        sys.exit('ONESIGNAL_API_KEY secret is missing')
    body = {'app_id': APP_ID, 'target_channel': 'push', 'included_segments': ['Total Subscriptions'],
            'headings': {'en': heading}, 'contents': {'en': text}, 'url': url, 'chrome_web_icon': ICON}
    if image:
        body['chrome_web_image'] = image
    try:
        r = get_json('https://api.onesignal.com/notifications?c=push',
                     {'Authorization': 'Key ' + key, 'Content-Type': 'application/json'},
                     json.dumps(body).encode())
    except urllib.error.HTTPError as e:
        sys.exit(f'OneSignal error {e.code}: {e.read().decode()[:500]}')
    errs = r.get('errors')
    if errs and 'not subscribed' not in json.dumps(errs).lower():
        sys.exit(f'OneSignal error: {errs}')
    print('Sent:', heading, '-', text, '| id', r.get('id'), '| note', errs or '')


def main():
    if '--test' in sys.argv:
        send('Forge2Forge', 'Test notification. If you can read this, notifications are working.', SITE)
        return
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    changed = False

    # new episodes
    try:
        eps = episodes()
    except Exception as e:
        print('YouTube check failed:', e)
        eps = None
    if eps is not None:
        if 'videos' not in state:
            state['videos'] = [e['id'] for e in eps]
            changed = True
            print('First run: recorded', len(eps), 'episodes, nothing sent')
        else:
            cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=MAX_AGE_DAYS)
            new = [e for e in eps if e['id'] not in state['videos']]
            for e in reversed(new):   # oldest first
                when = datetime.datetime.fromisoformat(e['date'].replace('Z', '+00:00'))
                if when >= cutoff:
                    send('New Forge2Forge Episode', e['title'], f"{SITE}?ep={e['id']}&source=push", e['thumb'])
                else:
                    print('Skipped old video', e['id'])
                state['videos'].append(e['id'])
                changed = True
            state['videos'] = state['videos'][-200:]

    # new resources
    res = resources()
    names = [r['name'] for r in res]
    if 'resources' not in state:
        state['resources'] = names
        changed = True
        print('First run: recorded', len(names), 'resources, nothing sent')
    else:
        new = [r for r in res if r['name'] not in state['resources']]
        if len(new) == 1:
            d = new[0]['desc']
            send('New Resource Added', new[0]['name'] + (': ' + (d[:117] + '…' if len(d) > 120 else d) if d else ''), SITE + '#resources')
        elif new:
            send('New Resources Added', ', '.join(r['name'] for r in new), SITE + '#resources')
        if new or set(state['resources']) != set(names):
            state['resources'] = names
            changed = True

    if changed:
        json.dump(state, open(STATE, 'w'), indent=1)
        print('State updated')
    else:
        print('Nothing new')


if __name__ == '__main__':
    main()
