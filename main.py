from executor import Executor
import config_logger

if __name__ == "__main__":
    config_logger.setup()

    exect = Executor()

    msg_data = {
        "my":"msg",
        "is": "awesome"
    }
    exect.execute(msg_data)

    # msg_data2 = {
    #         "my":"msg",
    #         "is": "awesome"
    # }
    # exect.execute(msg_data2)

    # msg_data3 = {
    #         "my":"msg",
    #         "is": "awesome"
    # }
    # exect.execute(msg_data3)
    input("") #waiting char to exit
        