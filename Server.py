import asyncio
from enum import Enum


class ServerPolicy(Enum) :
    INFINITY_QUEUE_SIZE = 1
    STRONG_QUEUE_SIZE = 2


class Server:
    def __init__(self, capacity=1000, server_policy = ServerPolicy.INFINITY_QUEUE_SIZE):
        self.capacity = capacity
        self._future = None
        self._Q = []  # очередь отправок получателям
        self._items = {}  # последние значения от отправителей
        self._subscriptions = {}  # подписанные получатели на отправителей
        self.is_process = True
        self.policy = server_policy

    def start(self):
        self.is_process = True
        self._future = asyncio.ensure_future(self._job())

    def send(self, publisher, message):
        self._items[publisher] = message
        if self.policy == ServerPolicy.INFINITY_QUEUE_SIZE:
            if publisher in self._subscriptions:
                for i in self._subscriptions[publisher]:
                    self._Q.insert(0, tuple((i, publisher, message)))
        elif self.policy == ServerPolicy.STRONG_QUEUE_SIZE:
            if publisher in self._subscriptions:
                for i in self._subscriptions[publisher]:
                    if len(self._Q) < self.capacity:
                        self._Q.insert(0, tuple((i, publisher, message)))

    async def _process_item(self, subs, publisher, message):
        subs.receive(publisher, message)

    async def _job(self):
        print ("START SERVER")
        while self.is_process or len(self._Q) > 0:
            await asyncio.sleep(0.05)
            if len(self._Q) > 0:
                if len(self._Q) % 100 == 0:
                    print("Server queue size is %d" % len(self._Q))
                sub, pub, message = self._Q.pop()
                await self._process_item(sub, pub, message)

    def stop(self):
        self.is_process = False
        print ("STOP SERVER queue size is %d" % len(self._Q))
        return self._future

    def subscribe(self, subs, publ):
        if publ not in self._subscriptions:
            self._subscriptions[publ] = []
        self._subscriptions[publ].append(subs)
