
from threading import Thread, main_thread
from persistqueue import SQLiteAckQueue
import uuid
from json_object import JsonObject
import logging

logger = logging.getLogger()

class Payload(JsonObject):
    # {'id': 'aaaaa', 'data': {'error': true}, 'retry': 0}
    # {'id': 'aaaaa', 'data': {'boa': 'noite'}, 'retry': 0}
    id:str
    data:dict
    retry:int

    def __init__(self, data:dict, id:str = None, retry:int = 0) -> None:
        self.data = data
        self.retry = retry
        if not id:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

    def __repr__(self) -> str:
        return self.to_json_string()

class Broker:
    q:SQLiteAckQueue = None
    do_work_func:None
    q_name:str = ""

    def __init__(self, q_name:str,do_work_func:callable = None, num_worker_threads:int=1) -> None:
        self.q = SQLiteAckQueue(path=f"{q_name}", multithreading=True)
        self.do_work_func = do_work_func
        self.q_name = q_name

        for i in range(num_worker_threads):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()
            
    def __main_thread_is_alive(self):
        return main_thread().is_alive()

    def worker(self):
        while True:
            if not self.__main_thread_is_alive():
                continue
            
            if self.q.active_size() == 0:
                continue
            
            # print("len", self.q.active_size())
            logger.info(f"Active size broker {self.q_name}: {self.q.active_size()}")

            item = self.q.get(raw=True)
            # print(item)
            if self.do_work_func:
                try:
                    self.do_work_func(self, item)
                except Exception as e:
                    self.q.nack(item)
                    logger.exception(e)

    def add(self, msg:Payload):
        return self.q.put(msg)

    def ack(self, item:dict):
        return self.q.ack(item)

    def ack_failed(self, item:dict):
        return self.q.ack_failed(item)

    def nack(self, item:dict):
        # payload:Payload = item["data"]
        # payload.retry = payload.retry + 1
        # item["data"] = payload
        # self.q.update(item)
        return self.q.nack(item)

if __name__ == "__main__":
    def do_work(broker:Broker, item:dict):
        timestamp = item["timestamp"]
        msg = item["data"]

        print(f"----- start -----\ndoing work: {type(item)} {type(msg)} {str(item)}\n{timestamp}\n----- end -----")

        if msg.retry >= 3:
            broker.ack_failed(item)
            return

        if 'error' in msg.data:
            broker.nack(item)
            return

        broker.ack(item)
            
    broker = Broker("main",do_work, 1)
    msg_data = {
        "zica":"opsss",
        "ola": "oi"
    }
    msg = Payload(msg_data)

    #print(msg.to_json_string())
    #print(Message.from_json_string(msg.to_json_string()).to_json_string())
    
    broker.add(msg)
    
    on = True
    while on:
        data = input("input:")
        print(f"data = {data}")
        if data == "exit" or data == "q":
            on = False
            break
        
        broker.add(Payload({f"{data}": "opa"}))

    exit(1)