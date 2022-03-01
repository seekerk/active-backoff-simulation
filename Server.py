import asyncio


class Server:
    def __init__(self, capacity=1000):
        self._future = None
        self._Q = []  # очередь отправок получателям
        self._items = {}  # последние значения от отправителей
        self._subscriptions = {}  # подписанные получатели на отправителей
        self.is_process = True

    def start(self):
        self._future = asyncio.ensure_future(self._job())


    def send(self, publisher, message):
        #print("Server got message %d from %d" % (message, publisher))
        self._items[publisher] = message
        if publisher in self._subscriptions:
            for i in self._subscriptions[publisher]:
                self._Q.insert(0, tuple((i, publisher, message)))
        #print("Server queue size is %d" % len(self._Q))

    async def _process_item(self, subs, publisher, message):
        subs.receive(publisher, message)

    async def _job(self):
        print ("START SERVER")
        while self.is_process:
            await asyncio.sleep(0.01)
            if len(self._Q) > 0:
                print("Server queue size is %d" % len(self._Q))
                sub, pub, message = self._Q.pop()
                await self._process_item(sub, pub, message)

        print ("STOP SERVER queue size is %d" % len(self._Q))

    def stop(self):
        self.is_process = False
        return self._future

    def subscribe(self, subs, publ):
        if publ not in self._subscriptions:
            self._subscriptions[publ] = []
        self._subscriptions[publ].append(subs)
