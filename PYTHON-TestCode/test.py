import asyncio
from multiprocessing import Process, Manager


class Loop:
    def __init__(self, name, running) -> None:
        self.name = name
        self.running = running
    
    def start(self):
        asyncio.run(self.loop())
        
    async def loop(self):
        while self.running.value:
            print("running : ", self.name)


if __name__ == "__main__":
    manager = Manager()
    running = manager.Value('b', True)
    loop1 = Loop("loop1", running)
    loop2 = Loop("loop2", running)
    
    process1 = Process(target=loop1.start)
    process2 = Process(target=loop2.start)
    
    process1.start()
    # process2.start()
    
    
    process1.join()
    # process2.join()
    print("end")