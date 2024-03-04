from executor import Executor
import config_logger
from task_service import WebHookTaskService
from notification_service import TelegramNotificationService

if __name__ == "__main__":
    config_logger.setup()

    webhook_service:WebHookTaskService = WebHookTaskService()
    telegram_service:TelegramNotificationService = TelegramNotificationService("3333333")

    exect = Executor(webhook_service, telegram_service)

    msg_data = {
        "url": "https://aaaaa.com/api/notify",
        "payload": {
            "my":"msg",
            "is": "awesome"
        }
    }
    exect.execute(msg_data)

    msg_data2 = {
            "my":"msg",
            "is": "awesome"
    }
    exect.execute(msg_data2)

    # msg_data3 = {
    #         "my":"msg",
    #         "is": "awesome"
    # }
    # exect.execute(msg_data3)
    input("") #waiting char to exit
        