import asyncio

from core import Server

if __name__ == '__main__':
    server = Server()
    server.address = '127.0.0.1'
    server.port = 8000
    asyncio.run(server.serve())

