import asyncio


class Subscriber:
    def __init__(self, server, num, pub_num):
        self.process = None
        self.message_num = 0
        self.error_count = 0
        self.server = server
        self.num = num
        self.publisher = pub_num
        server.subscribe(self, pub_num)

    pass

    def start(self):
        self.message_num = 0
        self.process = asyncio.ensure_future(self._job())

    def get_job(self):
        return self.process

    async def _job(self):
        while True:
            cur_msg_num = self.message_num  # запоминаем последний номер сообщения
            await asyncio.sleep(3)
            if cur_msg_num == self.message_num:  # если за время сна не изменился номер, то выходим
                break
        #print("Stop wait at Subscriber %d" % self.num)

    def receive(self, publ, message):
        self.error_count += message - self.message_num - 1
        self.message_num = message

    def stats(self):
        return self.message_num, self.error_count
