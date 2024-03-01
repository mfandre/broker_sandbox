from abc import ABC, abstractmethod 
import logging

logger = logging.getLogger()

class NotificationService(ABC):
    @abstractmethod
    def notify(self):
        """
        Método abstrato para enviar a notificação.
        """
        pass

    @abstractmethod
    def config(self):
        """
        Método abstrato para configurar a notificação (por exemplo, definir destinatários, mensagens, etc.).
        """
        pass

# Exemplo de implementação para notificação por e-mail
class EmailNotificationService(NotificationService):
    __from:str
    __to:str
    __body:str
    __subject:str

    def __init__(self, to, subject, body):
        self.__to = to
        self.__subject = subject
        self.__body = body

    def notify(self):
        # Lógica para enviar e-mail
        logger.info(f"Enviando e-mail... {self.__to}")
        

    def config(self):
        # Lógica para configurar e-mail
        logger.info("Configurando e-mail...")

# Exemplo de implementação para notificação por e-mail
class TelegramNotificationService(NotificationService):
    __phone_number:str
    __msg:str

    def __init__(self, phone_number:str, msg:str):
        self.__phone_number = phone_number
        self.__msg = msg

    def notify(self):
        # Lógica para enviar telegram
        logger.info(f"Enviando telegram... {self.__phone_number}")

    def config(self):
        # Lógica para configurar telegram
        logger.info("Configurando telegram...")


if __name__ == "__main__":
    email_notification = EmailNotificationService("zica@zica.com","zica", "zicou")
    email_notification.config()
    email_notification.notify()

    whatsapp_notification = TelegramNotificationService("+55219999999999","zicouuuu")
    whatsapp_notification.config()
    whatsapp_notification.notify()