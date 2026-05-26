import json
import urllib.request

repo = "im-anishraj/arnio"
url = f"https://api.github.com/repos/{repo}/actions/runs?branch=feat/issue-44-csv-optimizations&per_page=1"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if not data["workflow_runs"]:
            repo = "basantnema31/arnio"
            url = f"https://api.github.com/repos/{repo}/actions/runs?branch=feat/issue-44-csv-optimizations&per_page=1"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response2:
                data = json.loads(response2.read().decode())
        run_id = data["workflow_runs"][0]["id"]
        print(f"Latest run ID: {run_id}")

    jobs_url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs"
    req = urllib.request.Request(jobs_url)
    with urllib.request.urlopen(req) as response:
        jobs_data = json.loads(response.read().decode())
        failed_job = next(
            (j for j in jobs_data["jobs"] if j["conclusion"] == "failure"), None
        )
        if failed_job:
            print(f"Failed job: {failed_job['name']}")
            log_req = urllib.request.Request(failed_job["url"] + "/logs")
            try:
                with urllib.request.urlopen(log_req) as log_res:
                    lines = log_res.read().decode().splitlines()
                    print("\n".join(lines[-50:]))
            except Exception as e:
                print(f"Failed to fetch logs: {e}")
        else:
            print("No failed job found.")
except Exception as e:
    print(f"Error: {e}")
