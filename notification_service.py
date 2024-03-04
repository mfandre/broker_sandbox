from abc import ABC, abstractmethod 
import logging

logger = logging.getLogger()

class NotificationService(ABC):
    configed:bool = False

    def __init__(self):
        self.configed = False

    @abstractmethod
    def notify(self, str:str):
        """
        Método abstrato para enviar a notificação.
        """
        if not self.configed:
            raise RuntimeError("A notificação não foi configurada. Chame o método 'config' antes de enviar.")
        print("Enviando notificação...")

    @abstractmethod
    def config(self, *args, **kwargs):
        """
        Método abstrato para configurar a notificação (por exemplo, definir destinatários, mensagens, etc.).
        """
        self.configed = True

# Exemplo de implementação para notificação por e-mail
class EmailNotificationService(NotificationService):
    __server:str
    __port:str
    __user:str
    __pass:str
    __email_from:str

    def __init__(self, email_from:str, to:str, server:str, port:str, user:str, password:str):
        self.__server = server
        self.__port = port
        self.__user = user
        self.__pass = password
        self.__email_from = email_from
        self.__to = to

    def notify(self, msg:str):
        super().notify(msg)  # Chama o método da classe base
        # Lógica para enviar e-mail
        body = msg
        subject = "Alerting"
        logger.info(f"Enviando e-mail... {subject} {body}")
        

    def config(self, *args, **kwargs):
        super().config()
        # Lógica para configurar e-mail
        logger.info("Configurando e-mail...")

# Exemplo de implementação para notificação por e-mail
class TelegramNotificationService(NotificationService):
    __phone_number:str

    def __init__(self, phone_number):
        self.config(phone_number=phone_number)

    def notify(self, msg:str):
        super().notify(msg)  # Chama o método da classe base
        # Lógica para enviar telegram
        logger.info(f"Enviando telegram... {self.__phone_number} {msg}")

    def config(self, *args, **kwargs):
        super().config()
        
        self.__phone_number = kwargs["phone_number"]
        # Lógica para configurar telegram
        logger.info("Configurando telegram...")


if __name__ == "__main__":
    email_notification = EmailNotificationService("zica@zica.com","zica", "zicou")
    email_notification.config()
    email_notification.notify()

    whatsapp_notification = TelegramNotificationService("+55219999999999","zicouuuu")
    whatsapp_notification.config()
    whatsapp_notification.notify()