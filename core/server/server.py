import asyncio
from http.server import ThreadingHTTPServer

from core.server.http import RequestHandler


class Server:
    def __init__(self):
        self.address: str = ''
        self.port: int = 8000
        self.httpd = ThreadingHTTPServer((self.address, self.port), RequestHandler)

    async def serve(self) -> None:
        loop = asyncio.get_event_loop()
        server_coroutine = loop.run_in_executor(None, self.httpd.serve_forever)
        await server_coroutine
