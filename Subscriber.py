import asyncio


class Subscriber:
    def __init__(self, server, num, pub_num):
        self.message_count = None
        self.active_count = 0
        self.active_process = None
        self.timeout = None
        self.process = None
        self.message_num = 0
        self.error_count = 0
        self.server = server
        self.num = num
        self.publisher = pub_num
        server.subscribe(self, pub_num)

    pass

    def start(self):
        self.message_count = 0
        self.message_num = 0
        self.error_count = 0
        self.process = asyncio.ensure_future(self._job())
        self.timeout = 1
        self.active_count = 0
        self.active_process = asyncio.ensure_future(self._active_job())

    def get_job(self):
        return self.process

    async def _job(self):
        while True:
            cur_msg_num = self.message_num  # запоминаем последний номер сообщения
            await asyncio.sleep(3)
            if cur_msg_num == self.message_num:  # если за время сна не изменился номер, то выходим
                self.timeout = 0
                await self.active_process
                break

    async def _active_job(self):  # реализация активной подписки
        while self.timeout > 0:
            await asyncio.sleep(self.timeout)
            if self.timeout == 0:
                break
            val = await self.server.get(self.publisher)
            if val > self.message_num:
                # if val - self.message_num > 1:
                #     print("BINGO!!!! subs=%d, val=%d, prev=%d, errors:%d" % (self.num, val, self.message_num,
                #                                                              self.error_count))
                self.timeout /= 2
                self.error_count += val - self.message_num - 1
                self.message_num = val
                self.active_count += 1
            else:
                self.timeout += 0.1

    def receive(self, publ, message):
        if message <= self.message_num:
            return
        # print ("subs=%d, msg=%d, num=%d, error_val=%d, new=%d" % (self.num, message, self.message_num, self.error_count,
        #                                                           self.error_count + message - self.message_num - 1))
        self.error_count += message - self.message_num - 1
        self.message_num = message
        self.message_count += 1

    def stats(self):
        return self.message_count, self.error_count, self.active_count
