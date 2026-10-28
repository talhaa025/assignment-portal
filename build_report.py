import json, os, sys, datetime, requests

with open(".report.json") as f:
    raw = json.load(f)

tests = []
for t in raw.get("tests", []):
    message = ""
    if t["outcome"] != "passed":
        call = t.get("call", {})
        message = call.get("crash", {}).get("message", "") or call.get("longrepr", "")
    tests.append({
        "name": t["nodeid"],
        "result": t["outcome"],
        "failure_message": message,
    })

passed = sum(1 for t in tests if t["result"] == "passed")
total = len(tests)

report = {
    "repository": os.environ.get("GITHUB_REPOSITORY", "local"),
    "branch": os.environ.get("GITHUB_REF_NAME", "local"),
    "commit_sha": os.environ.get("GITHUB_SHA", "local"),
    "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "tests": tests,
    "summary": {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "status": "PASSED" if total > 0 and passed == total else "FAILED",
    },
}

url = os.environ.get("RECEIVER_URL", "http://127.0.0.1:5001")
response = requests.post(url, json=report, timeout=30)
print("Receiver responded:", response.status_code)
sys.exit(0 if response.ok else 1)