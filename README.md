# Assignment Submission Portal

A Flask portal where students submit their name, registration number, assignment title and a submission URL.
Every push is tested automatically with GitHub Actions, and the test report is sent to a local receiver.

## How to run the application
```
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## How to run the tests
```
python -m pytest
```

## How to start the receiver
```
python receiver.py
```
The receiver listens on http://127.0.0.1:5001 and saves each incoming report as `test-report.json`.

## CI pipeline
- Workflow: `.github/workflows/ci.yml`, triggered on every push.
- It runs on a self-hosted runner on my computer, so `localhost` reaches the receiver.
- `build_report.py` builds the JSON report (repository, branch, commit SHA, run id, timestamp, per-test results, totals, overall status) and POSTs it to the receiver. The step uses `if: always()`, so reports are sent for passing and failing runs.

## Start the runner
```
cd C:\actions-runner
.\run.cmd
```