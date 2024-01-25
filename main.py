import asyncio

from core import Server

if __name__ == '__main__':
    asyncio.run(Server().serve())

