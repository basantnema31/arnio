import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://api.github.com/repos/im-anishraj/arnio/pulls/987'
req = urllib.request.Request(url)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        print(f"PR Title: {data['title']}")
        print(f"State: {data['state']}")
        print(f"Mergeable: {data['mergeable']}")
        print(f"Mergeable state: {data['mergeable_state']}")
        
        # Check commit status
        statuses_url = data['statuses_url']
        statuses_req = urllib.request.Request(statuses_url)
        with urllib.request.urlopen(statuses_req, context=ctx) as s_response:
            s_data = json.loads(s_response.read().decode())
            print("\nStatuses:")
            for status in s_data:
                print(f"- {status['context']}: {status['state']} ({status['description']})")
except Exception as e:
    print(e)
