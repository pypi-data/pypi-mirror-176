import asyncio
from aiohttp import ClientSession
from time import time
from jsonrpc_websocket import Server

class TOMClient():
    def __init__(self, host_url):
        self.server = Server(f"ws://{host_url}/api/v1/ws")
        self.is_connected = False

    def update_status(self, ip_addr: str, metric: str, value: str):
        current_time = int(time())
        async def send_status():
            if not self.is_connected:
                await self.server.ws_connect()
                self.is_connected = True
            await self.server.worker_update(current_time, metric, value, ip_addr)
        asyncio.get_event_loop().run_until_complete(send_status())

    def join(self, worker_name: str, ip_addr: str, gpu_spec: str, gpu_memory: str):
        async def join_worker():
            if not self.is_connected:
                await self.server.ws_connect()
                self.is_connected = True
            await self.server.worker_join(worker_name, ip_addr, gpu_spec, gpu_memory)
        asyncio.get_event_loop().run_until_complete(join_worker())