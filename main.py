# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio

from Subscriber import Subscriber


class Publisher:
    def __init__(self, server, num):
        self.server = server
        self.num = num

    pass


class Server:
    pass


def createClients(publish_count=25, subscribe_count=25):
    server = Server()
    publishers = []
    for i in range(publish_count):
        client = Publisher(server, i)
        publishers.append(client)

    subscribers = []
    for i in range(subscribe_count):
        client = Subscriber(server, i, i % publish_count)
        subscribers.append(client)

    return server, publishers, subscribers


# Press the green button in the gutter to run the script.
async def startTesting(server, publishers, subscribers):
    for client in subscribers:
        client.start()

    for client in publishers:
        client.start()
    pass


def collectStats(server, publishers, subscribers):
    send_count = 0
    receive_count = 0
    error_count = 0
    for client in publishers:
        send_count += client.stats()
    print("Send:" + str(send_count))

    for client in subscribers:
        receive_num, receive_err = client.stats()
        receive_count += receive_num
        error_count += receive_err
    print("Receive %d items, %d errors", receive_count, error_count)

    pass


if __name__ == '__main__':
    cserver, cpublishers, csubscribers = createClients()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(startTesting(cserver, cpublishers, csubscribers))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

    collectStats(cserver, cpublishers, csubscribers)

