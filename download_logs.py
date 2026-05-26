import urllib.request
import json
import ssl
import zipfile
import io

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://api.github.com/repos/im-anishraj/arnio/actions/runs?branch=feat/issue-44-csv-optimizations&per_page=1'
req = urllib.request.Request(url)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        run = data['workflow_runs'][0]
        run_id = run['id']
        print(f"Run ID: {run_id}")
        
        logs_url = f"https://api.github.com/repos/im-anishraj/arnio/actions/runs/{run_id}/logs"
        print(f"Downloading logs from: {logs_url}")
        
        req_logs = urllib.request.Request(logs_url)
        with urllib.request.urlopen(req_logs, context=ctx) as log_res:
            zip_data = log_res.read()
            with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
                # Find a windows test log
                for name in z.namelist():
                    if "Test on windows-latest" in name and "Run pytest" in name:
                        print(f"\n--- Found log: {name} ---")
                        content = z.read(name).decode('utf-8', errors='ignore')
                        # Print last 50 lines to see the error
                        lines = content.split('\n')
                        print('\n'.join(lines[-100:]))
                        break
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}")
    if e.code == 403:
        print("Forbidden: You cannot download logs without auth.")
except Exception as e:
    print(e)
