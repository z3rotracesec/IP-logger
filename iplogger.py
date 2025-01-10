import http.server
import socketserver
import json
import urllib.request
from user_agents import parse

PORT = 80  # Port for listening
LOG_FILE = "visitor_device_info.txt"  # File to store visitor data

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Collect the IP address of the visitor
        client_ip = self.client_address[0]

        # Collect the User-Agent (browser and device information)
        user_agent = self.headers.get('User-Agent')
        parsed_ua = parse(user_agent)

        # Extract device details
        device_type = "Mobile" if parsed_ua.is_mobile else "Tablet" if parsed_ua.is_tablet else "Desktop"
        os = parsed_ua.os.family
        browser = parsed_ua.browser.family
        brand = parsed_ua.device.brand or "Unknown"
        model = parsed_ua.device.model or "Unknown"

        # Attempt to perform geolocation using ip-api.com
        try:
            url = f"http://ip-api.com/json/{client_ip}"
            response = urllib.request.urlopen(url)
            geo_data = json.loads(response.read().decode())
            location = f"{geo_data['city']}, {geo_data['country']}"
        except Exception:
            location = "Geolocation failed"

        # Log the data into a file
        with open(LOG_FILE, "a") as file:
            file.write(f"IP: {client_ip}\n")
            file.write(f"Device: {device_type}\n")
            file.write(f"OS: {os}\n")
            file.write(f"Browser: {browser}\n")
            file.write(f"Brand: {brand}\n")
            file.write(f"Model: {model}\n")
            file.write(f"Location: {location}\n")
            file.write("-" * 40 + "\n")

        # Print the data in the terminal for real-time monitoring
        print(f"IP: {client_ip}")
        print(f"Device: {device_type}")
        print(f"OS: {os}")
        print(f"Browser: {browser}")
        print(f"Brand: {brand}")
        print(f"Model: {model}")
        print(f"Location: {location}")

        # Respond to the client with a simple HTML message
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Data has been recorded successfully!</h1></body></html>")

# Start the server
def run_server():
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server is running on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
