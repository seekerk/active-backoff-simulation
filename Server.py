import asyncio
from enum import Enum


class ServerPolicy(Enum) :
    INFINITY_QUEUE_SIZE = 1
    STRONG_QUEUE_SIZE = 2


class Server:
    def __init__(self, capacity=100, server_policy = ServerPolicy.INFINITY_QUEUE_SIZE):
        self.capacity = capacity
        self._future = None
        self._Q = []  # очередь отправок получателям
        self._items = {}  # последние значения от отправителей
        self._subscriptions = {}  # подписанные получатели на отправителей
        self.is_process = True
        self.policy = server_policy
        self.max_queue_size = 0

    def start(self):
        self.is_process = True
        self.max_queue_size = 0
        self._future = asyncio.ensure_future(self._job())

    def send(self, publisher, message):
        self._items[publisher] = message

        # add new tasks to queue
        if self.policy == ServerPolicy.INFINITY_QUEUE_SIZE:
            if publisher in self._subscriptions:
                for i in self._subscriptions[publisher]:
                    self._Q.insert(0, tuple((i, publisher, message)))
        elif self.policy == ServerPolicy.STRONG_QUEUE_SIZE:
            if publisher in self._subscriptions:
                for i in self._subscriptions[publisher]:
                    if len(self._Q) < self.capacity:
                        self._Q.insert(0, tuple((i, publisher, message)))
        if len(self._Q) > self.max_queue_size:
            self.max_queue_size = len(self._Q)

    async def _process_item(self, subs, publisher, message):
        subs.receive(publisher, message)

    async def _job(self):
        while self.is_process or len(self._Q) > 0:
            await asyncio.sleep(0.01)
            if len(self._Q) > 0:
                # if len(self._Q) % 100 == 0:
                #     print("Server queue size is %d" % len(self._Q))
                sub, pub, message = self._Q.pop()
                if self._items[pub] == message:
                    await self._process_item(sub, pub, message)

    def stop(self):
        self.is_process = False
        print ("STOP SERVER, max queue size is %d" % self.max_queue_size)
        return self._future

    def subscribe(self, subs, publ):
        if publ not in self._subscriptions:
            self._subscriptions[publ] = []
        self._subscriptions[publ].append(subs)

    async def get(self, publ):
        await asyncio.sleep(0.01 * (1 + len(self._Q)))
        if publ in self._items:
            return self._items[publ]
        return 0
