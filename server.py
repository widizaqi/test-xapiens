from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json
import platform # used to get the system kernel version

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            # Set response status code to 200 (OK)
            self.send_response(200)
            # Set headers
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Write the response
            self.wfile.write(b'{"status": "OK"}')
        elif self.path == '/date':
            # set response status code to 200(ok)
            self.send_response(200)
            # set headers
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Get current date and time
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Create JSON response
            response = json.dumps({"date": current_date})
            # Write the response
            self.wfile.write(response.encode('utf-8'))
            
        else:
            # Respond with a 404 Not Found if the path is not /health
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error": "Not Found"}')
    
    def do_POST(self):
        if self.path == '/print':
            # Get content length to read the body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length) # read the body data
            try:
                # Parse the body as JSON
                json_data = json.loads(post_data)
                # Set response status code to 200 (ok)
                self.send_response(200)
                # set headers
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # Write the exact same JSON message back
                response = json.dumps(json_data)
                self.wfile.write(response.encode('utf-8'))
            except json.JSONDecodeError:
                # if parsing fails, return a 400 bad request
                self.send_response(400)
                self.send_header('COntent-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
        elif self.path == '/shell':
            # set response status code to 200 (ok)
            self.send_response(200)
            # set headers
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # get the current kernel version
            kernel_version = platform.uname().release
            # create JSON response
            response = json.dumps({"kernel version": kernel_version})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application-json')
            self.end_headers()
            self.wfile.write(b'{"error": "Not Found" }')
                

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
