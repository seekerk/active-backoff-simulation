import asyncio


class Publisher:
    def __init__(self, server, num):
        self.message_num = None
        self._process = False
        self.server = server
        self.num = num

    pass

    def start(self, message_num=10):
        self.message_num = message_num
        asyncio.ensure_future(self._job(message_num))

    async def _job(self, message_num):
        self._process = True
        for i in range(message_num):
            await asyncio.sleep(1)
            self.server.send(self.num, i + 1)
        self._process = False
        #print ("Publisher %d stopped" % self.num)

    def is_stop(self):
        return not self._process

    def stats(self):
        return self.message_num