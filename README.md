# Assignment Submission Portal

Flask portal for submitting name, registration number, assignment title and a submission URL.
Every push is tested automatically. The report is saved locally, emailed, and the demo site is deployed only if all tests pass.

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
Listens on http://127.0.0.1:5001 and saves each report as `test-report.json`.

## CI pipeline (`.github/workflows/ci.yml`)
- Runs on every push.
- `build_report.py` creates the JSON report (repository, branch, commit SHA, run id, timestamp, per-test results, totals, status) and POSTs it to the receiver. `if: always()` sends it for passing and failing runs.
- `send_email.py` emails the report. Credentials are GitHub secrets: `MAIL_USER`, `MAIL_PASS`, `MAIL_TO`, `MAIL_SERVER`.
- The `deploy` job publishes `docs/` to GitHub Pages and has `needs: test`, so failing tests leave the old site unchanged.

## Connecting CI to localhost
CI reaches the receiver through a Cloudflare tunnel (`cloudflared tunnel --url http://localhost:5001`) whose address is stored in the `RECEIVER_URL` secret.
(If using the self-hosted runner instead: `cd C:\actions-runner` then `.\run.cmd`.)

## Links
- Repository: https://github.com/talhaa025/assignment-portal
- Demo site: https://talhaa025.github.io/assignment-portal/