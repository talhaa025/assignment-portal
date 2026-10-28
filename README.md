# Assignment Submission Portal

## How to run the app
```
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
The CI job runs on a self-hosted runner on my computer, so it reaches the receiver at localhost.