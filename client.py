import websockets
import asyncio
import threading
global uri
class Client:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.connected = asyncio.Event()
        self.send_queue = asyncio.Queue()
    async def connect(self):
        while True:
            try:
                print("Connecting to server...")
                self.websocket = await websockets.connect(self.uri)
                self.connected.set()
                print("Connected to server.")
                asyncio.create_task(self.listen())
                asyncio.create_task(self.process_send_queue())
                break
            except Exception as e:
                print(f"Connection failed: {e}, retrying in 2s...")
                await asyncio.sleep(2)

    async def listen(self):
        global recievedData
        try:
            async for message in self.websocket:
                print(f"recieved: {message}")
                recievedData = message
        except Exception as e:
            print(f"Listen error: {e}")
        finally:
            self.connected.clear()
            await self.connect()

    async def process_send_queue(self):
        while True:
            await self.connected.wait()
            packet = await self.send_queue.get()
            try:
                await self.websocket.send(packet)
                #print(f"[SENT]: {packet}")
            except Exception as e:
                print(f"Send failed: {e}")

    async def send(self, packet):
        await self.send_queue.put(packet)



async def sendPacket(packet):
    await client.send(packet)

def startLoop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


#asyncio.run_coroutine_threadsafe(client.connect(), loop)
def set_location(name,port):
    uri = name
    port1 = port
def init():
    client = Client(uri)
    loop = asyncio.new_event_loop()
    threading.Thread(target=startLoop, args=(loop,), daemon=True).start()
def send(packet):
    return asyncio.run_coroutine_threadsafe(sendPacket(packet), loop)