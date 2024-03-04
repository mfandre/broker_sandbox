from broker import Payload, Broker
from random import randint, uniform
from datetime import datetime
import logging
from notification_service import NotificationService

from task_service import TaskService

logger = logging.getLogger()

class Executor:
    __main_broker:Broker = None
    __retry_broker:dict = None
    __dlq_broker:Broker = None
    __task:TaskService
    __notification:NotificationService
    __max_retries:int = 1
    def __init__(self,task_service, notification_service) -> None:
        self.__main_broker = Broker("main",self.main_consumer, 1)
        self.__retry_broker = Broker("retry",self.retry_consumer, 1)
        self.__dlq_broker = Broker("dlq",self.dlq_consumer, 1)
        self.__task = task_service
        self.__notification = notification_service

    def __is_ready(self):
        if not self.__main_broker:
            return False
        if not self.__retry_broker:
            return False
        if not self.__dlq_broker:
            return False
        return True

    def __exponential_backoff_calc(self, retry):
        backoff_in_seconds = 5
        sleep_in_seconds = (backoff_in_seconds * 7 ** retry + uniform(0, 1))
        
        # retry = 0 => 5s
        # retry = 1 => 35s
        # retry = 2 => 245s

        return sleep_in_seconds

    def main_consumer(self, broker:Broker, item:dict):
        if not self.__is_ready():
                return
        
        try:
            msg:Payload = item["data"]
            # print(f"----- start -----\nDoing work: {type(item)} {str(item)}\n----- end -----")
            logger.info(f"----- start -----\nDoing work ({msg.retry}): {type(item)} {str(item)}\n----- end -----")
            
            if self.__task.schema_is_valid(msg.data):
                self.__task.exec(msg.data)
                raise KeyError("Schema is not Valid")
            # if randint(0,100) <= 100: # randomizing error... 80% chance to error to test exponential backoff
            #     broker.ack_failed(item)
            #     if msg.retry < 3:
            #         self.__retry_broker.add(msg)
            #     else:
            #         self.__dlq_broker.add(msg)
            #     return
            
            broker.ack(item)
            logger.info(f"item acked: {str(item)}")
        except KeyError as ke:
            logger.exception(ke)
            self.__dlq_broker.add(msg)
        except Exception as e:
            logger.exception(e)
            broker.ack_failed(item)
            if msg.retry < self.__max_retries:
                self.__retry_broker.add(msg)
            else:
                self.__dlq_broker.add(msg)
        # msg.retry
        #broker.ack_failed(item)
        #broker.nack(item)
        #broker.ack(item)

    def retry_consumer(self, broker:Broker, item:dict):
        if not self.__is_ready():
            return
        try:
            msg:Payload = item["data"]
            timestamp = item["timestamp"]
            sleep_time = self.__exponential_backoff_calc(msg.retry)
            now = datetime.now().timestamp() 
            if timestamp + sleep_time >= now:
                logger.info(f"----- start -----\nRetry work sleeping backoff {msg.retry} {timestamp} {sleep_time} {now} \n----- end -----")
                #print(f"----- start -----\nRetry work sleeping backoff {msg.retry} {timestamp} {sleep_time} {now} \n----- end -----")
                broker.nack(item)
                return
            #print(f"----- start -----\nRetry work {msg.retry}: {type(item)} {str(item)}\n----- end -----")
            logger.info(f"----- start -----\nRetry work ({msg.retry}): {type(item)} {str(item)}\n----- end -----")
            msg.retry = msg.retry + 1
            self.__main_broker.add(msg)
            broker.ack(item)
        except Exception as e:
            broker.nack(item)
            logger.exception(e)
        #broker.ack_failed(item)
        #broker.nack(item)

    def dlq_consumer(self, broker:Broker, item:dict):
        if not self.__is_ready():
            return
        try:
            msg:Payload = item["data"]
            # print(f"----- start -----\nDLQ work: {type(item)} {str(item)}\n----- end -----")
            logger.info(f"----- start -----\nDLQ work ({msg.retry}): {type(item)} {str(item)}\n----- end -----")
            self.__notification.notify(msg=f"DLQ ({msg.retry}): {str(item)}")
            # msg.retry
            #broker.ack_failed(item)
            #broker.nack(item)
            broker.ack(item)
        except Exception as e:
            broker.nack(item)
            logger.exception(e)

    def execute(self, msg:dict):
        payload = Payload(msg)
        self.__main_broker.add(payload)