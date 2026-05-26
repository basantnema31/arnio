import urllib.request
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://api.github.com/repos/basantnema31/arnio/actions/runs?branch=feat/issue-44-csv-optimizations&per_page=1'
req = urllib.request.Request(url)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        if not data['workflow_runs']:
            print("No runs found.")
        else:
            run = data['workflow_runs'][0]
            print(f"Latest run ID: {run['id']}")
            print(f"Status: {run['status']}")
            print(f"Conclusion: {run['conclusion']}")
            print(f"HTML URL: {run['html_url']}")
            
            # Fetch jobs for this run
            jobs_url = run['jobs_url']
            jobs_req = urllib.request.Request(jobs_url)
            with urllib.request.urlopen(jobs_req, context=ctx) as jobs_response:
                jobs_data = json.loads(jobs_response.read().decode())
                print("\nJob Statuses:")
                for job in jobs_data['jobs']:
                    print(f"- {job['name']}: {job['status']} / {job['conclusion']}")
except Exception as e:
    print(e)
