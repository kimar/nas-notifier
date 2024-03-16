import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import requests
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),
    **os.environ,
}

host = config.get('HOST') or '0.0.0.0'
port = int(config.get('PORT') or 3000)
title = config.get('NOTIFICATION_TITLE') or 'nas-notifier'

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
      query_components = parse_qs(urlparse(self.path).query)
      text = query_components.get('text') or 'NO TEXT'

      r = requests.post('https://api.pushbullet.com/v2/pushes', headers={'Access-Token': config.get('PUSHBULLET_API_KEY')}, data={
        "type": "note",
        "title": title,
        "body": text
      })

      response = 'OK' if r.status_code == 200 else 'Error'

      self.send_response(200)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      self.wfile.write(response.encode())

server = HTTPServer((host, port), requestHandler)
print('Server listening on', host + ':' + str(port))

server.serve_forever()