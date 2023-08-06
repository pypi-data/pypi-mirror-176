#!/usr/bin/env python3
import configparser
import datetime
import json
import pathlib
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    from pynotifier import Notification
except Exception:
    pass

CREDS = pathlib.Path.home() / ".aws" / "credentials"
KEYS = ["aws_access_key_id", "aws_secret_access_key", "aws_session_token"]
KEY_MAP = {
    "aws_access_key_id": "AccessKeyId",
    "aws_secret_access_key": "SecretAccessKey",
    "aws_session_token": "SessionToken",
}


class RefreshServer(HTTPServer):
    pass


class RefreshHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Make logging a no-op"""
        return

    def do_GET(self):
        path = [p for p in self.path.split("/") if p]
        path = path[-1] if path else ""
        try:
            Notification(
                title="Credentials Needed!",
                description=f"Get creds for {path}",
                duration=120,
                urgency="critical",
            ).send()
        except NameError:
            pass
        input(f"Refresh credentials for {path} and then press enter.")
        cp = configparser.ConfigParser()
        cp.read(CREDS)
        creds = {KEY_MAP[k]: cp[path][k] for k in KEYS}
        creds["Version"] = 1
        creds["Expiration"] = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=58)
        ).isoformat()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(json.dumps(creds).encode("utf-8"))
        print("Waiting for credential refresh requests")


def creds_refresher():
    try:
        print("Waiting for credential refresh requests")
        web_server = RefreshServer(("127.0.0.1", 10100), RefreshHandler)
        web_server.serve_forever()
    except socket.error:
        print("Failed to start the credential refresher on required TCP port 10100")
        sys.exit(1)


if __name__ == "__main__":
    creds_refreshser()
