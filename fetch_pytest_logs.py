import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://api.github.com/repos/im-anishraj/arnio/pulls/987')
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        sha = data['head']['sha']
        
        checks_url = f"https://api.github.com/repos/im-anishraj/arnio/commits/{sha}/check-runs"
        checks_req = urllib.request.Request(checks_url)
        with urllib.request.urlopen(checks_req, context=ctx) as c_response:
            c_data = json.loads(c_response.read().decode())
            for check in c_data['check_runs']:
                if check['status'] == 'completed' and check['conclusion'] == 'failure' and 'Test on' in check['name']:
                    print(f"Check ID: {check['id']}")
                    print(f"Name: {check['name']}")
                    print(f"Output text: {check.get('output', {}).get('text')}")
                    
                    # Try to fetch logs if available
                    log_url = f"https://api.github.com/repos/im-anishraj/arnio/actions/jobs/{check['id']}/logs"
                    log_req = urllib.request.Request(log_url)
                    try:
                        with urllib.request.urlopen(log_req, context=ctx) as l_resp:
                            print("\nLog Tail:")
                            log_content = l_resp.read().decode('utf-8', errors='ignore')
                            lines = log_content.split('\n')
                            for i, line in enumerate(lines):
                                if 'fail' in line.lower() or 'exception' in line.lower() or 'error' in line.lower():
                                    if '====' in line or '___' in line:
                                        start = max(0, i-5)
                                        end = min(len(lines), i+30)
                                        print('\n'.join(lines[start:end]))
                                        break
                    except Exception as le:
                        print(f"Failed to fetch detailed log: {le}")
                    break
except Exception as e:
    print(e)
