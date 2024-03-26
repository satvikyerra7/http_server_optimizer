from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import parse_qs, urlparse

PORT = 8080
DATA_DIR = "/tmp/data"

class DataHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Validate and get filename
        filename = query_params.get("n", [None])[0]
        if not filename:
            self.send_error(400, "Missing filename parameter (n)")
            return

        # Validate and get line number (optional)
        line_number_str = query_params.get("m", [None])[0]
        if line_number_str:
            try:
                line_number = int(line_number_str)
            except ValueError:
                self.send_error(400, "Invalid line number format")
                return
        else:
            line_number = None

        # Build file path
        file_path = os.path.join(DATA_DIR, filename + ".txt")

        # Check if file exists
        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return

        # Read file content
        try:
            with open(file_path, "r") as f:
                if line_number is not None:
                    # Return specific line
                    content = f.readlines()[line_number - 1]
                else:
                    # Return entire file content
                    content = f.read()
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")
            return

        # Set response headers and send content
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

def main():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, DataHandler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
