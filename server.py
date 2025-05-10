import asyncio
import websockets

global uri
global port
connected_clients = set()

async def handle(websocket):
    connected_clients.add(websocket)
    print(f"new user: {len(connected_clients)}")
    try:
        async for message in websocket:
            print(f"client sent: {message}")
            others = connected_clients - {websocket}
            if others:
                await asyncio.gather(*(client.send(str(message)) for client in others))
    except websockets.exceptions.ConnectionClosed:
        print("clients connetion closed")
    finally:
        connected_clients.remove(websocket)
        print(f"clients left: {len(connected_clients)}")
async def handle_connection():
    async with websockets.serve(handle, uri, port):
        print("Server running")
        await asyncio.Future()
def set_location(name,port):
    uri = name
    port1 = port
    #return "ws://"+uri+":"+port1
def init():
    asyncio.run(handle_connection())
