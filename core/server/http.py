import re
from http import HTTPStatus, HTTPMethod
from http.server import SimpleHTTPRequestHandler
from os import PathLike
from typing import Callable, Any
from urllib.parse import urlparse, parse_qs

from core.templates.template import BaseTemplate
from core.values import *


class RequestHandler(SimpleHTTPRequestHandler):
    directories: dict = {STATIC_URL: STATIC_DIR, MEDIA_URL: MEDIA_DIR}
    prefixes: list[str] = [prefix for prefix, _ in directories.items()]
    urls: list[tuple[re.Pattern[str], Callable]] = []

    def list_directory(self, path: str | PathLike[str]) -> None:
        self._send_err_response(HTTPStatus.NOT_FOUND)

    def _send_head(self, status: HTTPStatus) -> None:
        self.send_response(status.value, status.phrase)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _send_err_response(self, status: HTTPStatus = HTTPStatus.NOT_FOUND) -> None:
        self._send_head(status)
        self.wfile.write(BaseTemplate('', {}).error(status).encode('UTF-8'))

    def do_GET(self) -> None:
        if any(self.path.startswith(pre) for pre in self.prefixes):
            return self._handle_file_request()
        url = urlparse(self.path)
        response = self._get_response(HTTPMethod.GET, url.path, url.query)
        if not response:
            return self._send_err_response()
        self._send_head(HTTPStatus.ACCEPTED)
        self.wfile.write(response().encode('UTF-8'))

    def do_POST(self) -> None:
        query = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        response = self._get_response(HTTPMethod.POST, urlparse(self.path).path, query)
        if not response:
            return self._send_err_response()
        self._send_head(response())

    def do_DELETE(self) -> None:
        url = urlparse(self.path)
        response = self._get_response(HTTPMethod.DELETE, url.path, url.query)
        if not response:
            return self._send_err_response()
        self._send_head(response())

    def translate_path(self, path: str) -> str:
        for prefix, directory in self.directories.items():
            if path.startswith(prefix):
                return str(Path(directory) / path[len(prefix):].lstrip('/'))
        return super().translate_path(path)

    def _handle_file_request(self):
        file = self.send_head()
        if not file:
            return
        self.copyfile(file, self.wfile)
        file.close()

    def _get_response(self, method: str, path, query) -> Any:
        response = None
        for route_pattern, route_class in self.urls:
            if route_pattern.fullmatch(path):
                continue
            response = getattr(route_class(path, parse_qs(query)), method.lower(), None)
        return response
