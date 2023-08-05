# This is a basic solution for getting the access token from an OAuth 2 server.
# When you want to grant a piece of software access to an API, you often need
# to open a web browser, go to that API, authorise the access, and you are then
# redirected to a new URL with the appropriate access token passed in the request.
# This works fine for web apps, but command-line ones won't normally be exposing
# a URL to which OAuth can redirect. To make it worse, many APIs will require a
# proper HTTPS URL.
#
# One solution to this is to use the very handy 'ngrok' utility. (ngrok.com)
# This allows you to expose, temporarily, a service running on your local machine
# as a publicly-accessible URL. So we run a simple server as a background thread,
# put ngrok in front of it, make the ngrok HTTPS url available so it can be specified
# as the redirection address, and then make the token available when it comes through.

import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

LOCAL_SERVER_PORT = 8584

try:
    from pyngrok import ngrok
except ImportError:
    print(
        "ngrok module not found. You probably need to 'pip install ngrok'.",
        file=sys.stderr
    )
    sys.exit(1)


class CollectorException(Exception):
    pass


class TokenReceivingServer(HTTPServer):
    """
    A simple HTTP server that listens on the specified port
    and stores the URL of the last request it received.
    """
    def __init__(self, port):
        self.received_request = None
        print("Starting a small HTTP server to receive the callback")
        super().__init__(('', port), TokenHandler)

    def save_request(self, request: str):
        self.received_request = request

    def last_request(self) -> str:
        return self.received_request


class TokenHandler(BaseHTTPRequestHandler):
    """
    A little HTTP request handler which expects a token
    and stores it in the server.
    """
    def do_GET(self):
        self.server.save_request(self.path)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(
            "Thank you.  Authentication token received. You can close this window.".encode()
        )


class TokenCollector():

    def __init__(self):
        self.http_server = TokenReceivingServer(LOCAL_SERVER_PORT)
        print("Starting ngrok to create an accessible HTTPS endpoint")
        self.ngrok = ngrok.connect(LOCAL_SERVER_PORT, bind_tls="true")

    def get_url(self):
        return self.ngrok.public_url
    
    def get_single_request(self):
        # Could make this wait until we have something that looks like a token
        print("Waiting for the callback...")
        self.http_server.handle_request()
        print("Got", self.http_server.last_request())

