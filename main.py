# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio

from Publisher import Publisher
from Server import Server, ServerPolicy
from Subscriber import Subscriber


def createClients(publish_count=25, subscribe_count=25, server_policy = ServerPolicy.INFINITY_QUEUE_SIZE):
    server = Server(server_policy)
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
    server.start()

    for client in subscribers:
        client.start()

    for client in publishers:
        client.start()

    while True :
        await asyncio.sleep(1)
        ready_to_stop = True
        for i in publishers:
            if i.is_stop():
                continue
            ready_to_stop = False
            break
        if ready_to_stop :
            break
    print("All publishers are done!")
    task = server.stop()
    for i in subscribers:
        await i.get_job()
    await task


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
    print("Receive %d items, %d errors" % (receive_count, error_count))

    pass


def appendSubscribes(server, subscribers, publish_count, append_num):
    for i in range(len(subscribers), len(subscribers) + append_num):
        client = Subscriber(server, i, i % publish_count)
        subscribers.append(client)
    return subscribers
    pass


if __name__ == '__main__':
    cserver, cpublishers, csubscribers = createClients(server_policy = ServerPolicy.STRONG_QUEUE_SIZE)

    i = 0

    while i < 100 :
        print("PROCESS publishers: %d, subscribers: %d" % (len(cpublishers), len(csubscribers)))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(startTesting(cserver, cpublishers, csubscribers))
            collectStats(cserver, cpublishers, csubscribers)
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

        csubscribers = appendSubscribes(cserver, csubscribers, len(cpublishers), 5)
        i += 1
