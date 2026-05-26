import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://api.github.com/search/issues?q=repo:im-anishraj/arnio+is:open+no:assignee+label:"status:%20ready"')
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        print(f"Found {data['total_count']} open, unassigned, 'status: ready' issues in arnio.")
        for item in data.get('items', [])[:10]:
            print(f"- {item['html_url']}: {item['title']}")
except Exception as e:
    print(e)
