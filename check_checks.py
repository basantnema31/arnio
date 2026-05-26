import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# We need the commit SHA to query the checks API
url = 'https://api.github.com/repos/im-anishraj/arnio/pulls/987'
req = urllib.request.Request(url)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        sha = data['head']['sha']
        
        checks_url = f"https://api.github.com/repos/im-anishraj/arnio/commits/{sha}/check-runs"
        checks_req = urllib.request.Request(checks_url)
        with urllib.request.urlopen(checks_req, context=ctx) as c_response:
            c_data = json.loads(c_response.read().decode())
            print(f"Total checks: {c_data['total_count']}")
            for check in c_data['check_runs']:
                print(f"- {check['name']}: {check['status']} / {check['conclusion']}")
except Exception as e:
    print(e)
