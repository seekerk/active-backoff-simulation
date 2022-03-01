import asyncio


class Subscriber:
    def __init__(self, server, num, pub_num):
        self.message_num = 0
        self.server = server
        self.num = num
        self.publisher = pub_num

    pass

    def start(self):
        self.message_num = 0
        asyncio.ensure_future(self._job())

    async def _job(self):
        while True:
            cur_msg_num = self.message_num  # запоминаем последний номер сообщения
            await asyncio.sleep(3)
            if cur_msg_num == self.message_num:  # если за время сна не изменился номер, то выходим
                break
        print("Stop wait at Subscriber %d", self.num)

