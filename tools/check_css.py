import os

for p in ['css/tablet-12-7.css', 'nsejs/css/wpe-touch-parity.css', 'site.css']:
    if os.path.exists(p):
        txt = open(p, encoding='utf-8').read()
        print(p, "length:", len(txt), "has topic-pill-btn:", "topic-pill-btn" in txt)
    else:
        print(p, "does not exist")
