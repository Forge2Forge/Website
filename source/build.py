# Build site/index.html from template.html and stamp a new version.
import base64, json, datetime
import os
B=os.path.dirname(os.path.abspath(__file__))+'/'
OUT=os.path.abspath(B+'..')+'/'
v=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S')
t=open(B+'template.html').read()
d=lambda f,m:'data:'+m+';base64,'+base64.b64encode(open(B+f,'rb').read()).decode()
for k,f,m in [('LOGO','icon.webp','image/webp'),('HERO','hero.webp','image/webp'),('STUDIO','studio.webp','image/webp'),('TWO','two.png','image/png'),('SHIELDMASK','shieldmask.webp','image/webp'),('SHJ','shield-J.webp','image/webp'),('SHT','shield-T.webp','image/webp')]:
    t=t.replace('{{'+k+'}}',d('assets/'+f,m))
t=t.replace('{{SITE_VERSION}}',v)
assert '{{' not in t
open(OUT+'index.html','w').write(t)
json.dump({'v':v},open(OUT+'version.json','w'))
print('version',v)
