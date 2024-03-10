import re
from http import HTTPStatus, HTTPMethod
from http.server import SimpleHTTPRequestHandler
from os import PathLike
from typing import Callable, Pattern
from urllib.parse import urlparse, parse_qs

from core.templates.template import BaseTemplate
from core.values import *


class RequestHandler(SimpleHTTPRequestHandler):
    directories: dict = {STATIC_URL: STATIC_DIR, MEDIA_URL: MEDIA_DIR}
    prefixes: list[str] = [prefix for prefix, _ in directories.items()]
    urls: dict[Pattern, Callable] = {}

    def list_directory(self, path: str | PathLike[str]) -> None:
        self.send_error(HTTPStatus.NOT_FOUND)

    def _send_head(self, status: HTTPStatus) -> None:
        self.send_response(status.value, status.phrase)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_error(self, code: HTTPStatus = HTTPStatus.NOT_FOUND, message: str = None, explain: str = None) -> None:
        self._send_head(code)
        self.wfile.write(BaseTemplate('', {}).error(code).encode('UTF-8'))

    def do_GET(self) -> None:
        if any(self.path.startswith(pre) for pre in self.prefixes):
            return self._handle_file_request()
        url = urlparse(self.path)
        self._respond(HTTPMethod.GET, url.path, url.query)

    def do_POST(self) -> None:
        query = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        self._respond(HTTPMethod.POST, urlparse(self.path).path, query)

    def do_DELETE(self) -> None:
        url = urlparse(self.path)
        self._respond(HTTPMethod.DELETE, url.path, url.query)

    def translate_path(self, path: str) -> str:
        for prefix, directory in self.directories.items():
            if path.startswith(prefix):
                return str(Path(directory) / path[len(prefix):].lstrip('/'))
        return super().translate_path(path)

    def _handle_file_request(self) -> None:
        file = self.send_head()
        if not file:
            return
        self.copyfile(file, self.wfile)
        file.close()

    def _respond(self, method: str, path: str, query: str) -> None:
        for route_pattern, route_class in self.urls.items():
            if route_pattern.fullmatch(path):
                response = getattr(route_class(path, parse_qs(query)), method.lower(), None)
                if not response:
                    return self.send_error()
                if isinstance(response(), HTTPStatus):
                    return self._send_head(response())
                self._send_head(HTTPStatus.ACCEPTED)
                self.wfile.write(response().encode('UTF-8'))
                return
        self.send_error(HTTPStatus.NOT_FOUND)
