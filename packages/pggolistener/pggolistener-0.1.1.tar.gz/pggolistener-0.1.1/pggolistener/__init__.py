import asyncio
import ctypes
import logging
import os
import threading
import time
from ctypes import Structure, c_char_p, c_int, c_wchar_p
import fcntl
import platform
import queue

_AIX = platform.system() == 'AIX'
_DARWIN = platform.system() == 'Darwin'
_LINUX = platform.system() == 'Linux'
_WINDOWS = platform.system() == 'Windows'

if _WINDOWS:
    golib = ctypes.cdll.LoadLibrary('./sub.dll')
else:
    golib = ctypes.cdll.LoadLibrary('./sub.so')


class sub_worker(object):
    def __init__(self, user, password, host, port, dbname, notify_name):
        self.user, self.password, self.host, self.port, self.dbname, self.notify_name = \
            user, password, host, port, dbname, notify_name

        self.r_pip, self.w_pip, self.loop, self.transport = None, None, None, None
        self.is_running = False
        self.events = queue.Queue()

    def start(self):
        if self.is_running:
            return
        r, w = os.pipe()
        self.r_pip, self.w_pip = r, w
        flags = fcntl.fcntl(w, fcntl.F_GETFL)
        flags = flags | os.O_NONBLOCK
        fcntl.fcntl(w, fcntl.F_SETFL, flags)
        t = threading.Thread(target=self.call_golang_sub_work)
        t.setDaemon(True)
        t.start()

        self.is_running = True
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.read_pip())
        self.loop.run_forever()

    def call_golang_sub_work(self):
        golib.SubWorkStart(self.w_pip,
                           self.user.encode('UTF-8'),
                           self.password.encode('UTF-8'),
                           self.host.encode('UTF-8'),
                           self.port,
                           self.dbname.encode('UTF-8'),
                           self.notify_name.encode('UTF-8'))

    async def read_pip(self):
        r = os.fdopen(self.r_pip)
        loop = self.loop
        reader = asyncio.StreamReader(loop=loop)
        protocol = asyncio.StreamReaderProtocol(reader)
        transport, _ = await loop.connect_read_pipe(lambda: protocol, r)
        while True:
            data = b''
            print("开始等待读")
            dumpLenBy = await reader.read(4)
            dumpLen = int.from_bytes(dumpLenBy, "big", signed=True)
            if dumpLen < 0:
                logging.info("关闭")
                loop.stop()
                return
            logging.info(f"事件长度:{dumpLen}")
            while True:
                if len(data) >= dumpLen:
                    break
                out = await reader.read(dumpLen)
                if out is None:
                    break
                else:
                    data += out
            print("++++++", data)
            self.events.put(data)

    def get_event(self):
        while True:
            yield self.events.get()

    def close(self):
        with os.fdopen(self.w_pip, 'wb') as w:
            w.write(int.to_bytes(-1, 4, 'big', signed=True))
        time.sleep(1)
        self.loop.close()
        return

# if __name__ == '__main__':
#     worker = sub_worker('postgres', '123456', '127.0.0.1', 5432, 'skq', 'event_from_golang')
#     t = threading.Thread(target=r, args=[worker])
#     t.setDaemon(True)
#     t.start()
#     worker.start()

#     print(platform.system())
#     # print(str())
#     # print(int.from_bytes(int.to_bytes(1000, 4, 'big', signed=True), 'big', signed=True))
