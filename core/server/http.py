from http import HTTPStatus, HTTPMethod
from http.server import SimpleHTTPRequestHandler
from os import PathLike
from urllib.parse import urlparse, parse_qs

from core.decorators import suppress_connection_errors
from core.server.routes import urls, url_route
from core.templates import base_template
from core.values import *


class RequestHandler(SimpleHTTPRequestHandler):
    directories: dict = {STATIC_URL: STATIC_DIR, MEDIA_URL: MEDIA_DIR}
    prefixes: list[str] = [prefix for prefix, _ in directories.items()]
    routes = url_route.construct_routes(urls)

    def list_directory(self, path: str | PathLike[str]) -> None:
        self.send_error(HTTPStatus.NOT_FOUND)

    def _send_head(self, status: HTTPStatus) -> None:
        self.send_response(status.value, status.phrase)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_error(self, code: HTTPStatus = HTTPStatus.NOT_FOUND, message: str = None, explain: str = None) -> None:
        self._send_head(code)
        self.wfile.write(base_template.error(code).encode('UTF-8'))

    @suppress_connection_errors
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

    @suppress_connection_errors
    def _handle_file_request(self) -> None:
        file = self.send_head()
        if not file:
            return
        self.copyfile(file, self.wfile)
        file.close()

    @suppress_connection_errors
    def _respond(self, method: str, path: str, query: str) -> None:
        for route_pattern, meta in self.routes.items():
            if route_pattern.fullmatch(path):
                route_class, params = meta
                response = getattr(route_class(path, parse_qs(query), params), method.lower(), None)
                if not response:
                    return self.send_error()
                response = response()
                if isinstance(response, HTTPStatus):
                    return self._send_head(response)
                self._send_head(HTTPStatus.ACCEPTED)
                self.wfile.write(response.encode('UTF-8'))
                return
        self.send_error(HTTPStatus.NOT_FOUND)
