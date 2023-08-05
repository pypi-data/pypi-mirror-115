import os
import asyncio
import signal
from typing import List, Dict, Any, cast

from .connect import write_connection_file, launch_kernel, connect_channel
from .message import receive_message, send_message


class KernelServer:
    def __init__(
        self,
        kernelspec_path: str = "",
        connection_file: str = "",
        capture_kernel_output: bool = True,
    ) -> None:
        self.capture_kernel_output = capture_kernel_output
        self.kernelspec_path = kernelspec_path
        if not self.kernelspec_path:
            raise RuntimeError(
                "Could not find a kernel, maybe you forgot to install one?"
            )
        self.connection_file_path, self.connection_cfg = write_connection_file(
            connection_file
        )
        self.key = cast(str, self.connection_cfg["key"])
        self.msg_cnt = 0
        self.execute_requests: Dict[str, Any] = {}
        self.stopped = asyncio.Event()
        self.connected_to_kernel = False
        self.channel_tasks: List[asyncio.Task] = []
        self.sessions: Dict[str, Any] = {}

    async def start(self) -> None:
        self.kernel_process = await launch_kernel(
            self.kernelspec_path, self.connection_file_path, self.capture_kernel_output
        )
        self.shell_channel = connect_channel("shell", self.connection_cfg)
        self.iopub_channel = connect_channel("iopub", self.connection_cfg)

    async def stop(self) -> None:
        self.kernel_process.send_signal(signal.SIGINT)
        self.kernel_process.kill()
        await self.kernel_process.wait()
        os.remove(self.connection_file_path)
        for task in self.channel_tasks:
            task.cancel()
        self.stopped.set()

    async def serve(self, websocket, session_id):
        self.sessions[session_id] = websocket
        if not self.connected_to_kernel:
            self.channel_tasks += [
                asyncio.create_task(self.listen_channel("shell")),
                asyncio.create_task(self.listen_channel("iopub")),
            ]
            self.connected_to_kernel = True
        self.channel_tasks += [asyncio.create_task(self.listen_web(websocket))]
        await self.stopped.wait()

    async def listen_web(self, websocket):
        while True:
            msg = await websocket.receive_json()
            if msg["channel"] == "shell":
                msg = {
                    "header": msg["header"],
                    "msg_id": msg["header"]["msg_id"],
                    "msg_type": msg["header"]["msg_type"],
                    "parent_header": msg["parent_header"],
                    "content": msg["content"],
                    "metadata": msg["metadata"],
                }
                send_message(msg, self.shell_channel, self.key)

    async def listen_channel(self, channel_name):
        channel = {"shell": self.shell_channel, "iopub": self.iopub_channel}[
            channel_name
        ]
        while True:
            msg = await receive_message(channel)
            msg["channel"] = channel_name
            session = msg["parent_header"]["session"]
            websocket = self.sessions[session]
            await websocket.send_json(msg)
