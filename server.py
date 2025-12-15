import asyncio
import websockets
import os

EMITTER = None
RECEIVER = None

async def handler(ws):
    global EMITTER, RECEIVER

    role = await ws.recv()  # "EMITTER" o "RECEIVER"

    if role == "EMITTER":
        EMITTER = ws
        print("Emisor conectado")

    elif role == "RECEIVER":
        RECEIVER = ws
        print("Receptor conectado")

    try:
        async for msg in ws:
            if ws == EMITTER and RECEIVER:
                await RECEIVER.send(msg)

            elif ws == RECEIVER and EMITTER:
                await EMITTER.send(msg)

    except:
        pass

async def main():
    port = int(os.environ.get("PORT", 10000))
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

asyncio.run(main())
