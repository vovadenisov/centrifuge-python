import time
import json
import asyncio
from centrifuge import Client, Credentials
from cent import generate_token


async def run():

    # Generate credentials.
    # In production this must only be done on backend side and you should
    # never show secret to client!
    user = "3000"
    timestamp = str(int(time.time()))
    info = json.dumps({"first_name": "Python", "last_name": "Client"})
    token = generate_token("secret", user, timestamp, info=info)

    credentials = Credentials(user, timestamp, info, token)
    address = "ws://localhost:8000/connection/websocket"

    async def connect_handler(**kwargs):
        print("Connected", kwargs)

    async def disconnect_handler(**kwargs):
        print("Disconnected:", kwargs)

    async def connect_error_handler(**kwargs):
        print("Error:", kwargs)

    client = Client(
        address, credentials,
        on_connect=connect_handler,
        on_disconnect=disconnect_handler,
        on_error=connect_error_handler
    )

    await client.connect()

    async def message_handler(**kwargs):
        print("Message:", kwargs)

    async def join_handler(**kwargs):
        print("Join:", kwargs)

    async def leave_handler(**kwargs):
        print("Leave:", kwargs)

    async def error_handler(**kwargs):
        print("Sub error:", kwargs)

    sub = await client.subscribe(
        "public:chat",
        on_message=message_handler,
        on_join=join_handler,
        on_leave=leave_handler,
        on_error=error_handler
    )

    success = await sub.publish({})
    print("Publish successful:", success)

    history = await sub.history()
    print("Channel history:", history)

    presence = await sub.presence()
    print("Channel presence:", presence)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("interrupted")
    finally:
        loop.close()
