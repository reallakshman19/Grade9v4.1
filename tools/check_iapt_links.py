import urllib.request, ssl, re

url = 'https://iapt.org.in/nse-2024-25/'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print('Page fetched, length:', len(html))
        pdf_links = re.findall(r'href=["\']([^"\']+\.pdf)["\']', html, re.I)
        print('Total PDF links found:', len(pdf_links))
        for l in pdf_links:
            if 'nse' in l.lower() or 'key' in l.lower() or 'js' in l.lower():
                print('PDF:', l)
except Exception as e:
    print('Error:', e)
