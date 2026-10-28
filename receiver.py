import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"invalid json")
            return
        with open("test-report.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Report received ->", data["summary"]["status"],
              "| commit", str(data["commit_sha"])[:7])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"saved")

if __name__ == "__main__":
    print("Receiver listening on http://127.0.0.1:5001 ...")
    HTTPServer(("127.0.0.1", 5001), Handler).serve_forever()