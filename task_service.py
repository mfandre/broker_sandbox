from abc import ABC, abstractmethod 
import logging

logger = logging.getLogger()


class TaskService(ABC):

    @abstractmethod
    def exec(self, *args, **kwargs):
        """
        Método abstrato para executar a task
        """
    
    @abstractmethod
    def schema_is_valid(self, *args, **kwargs) -> bool:
        """
        Método abstrato para avaliar schema da msg que será processada pelo serviço
        """

# Exemplo de implementação para notificação por e-mail
class WebHookTaskService(TaskService):

    def exec(self, *args, **kwargs):
        url = args[0]["url"]
        logger.info(f"Exec WebHook {url}")

    def schema_is_valid(self, *args, **kwargs) -> bool:
        if "url" not in args[0]:
            logger.warning(f"Schema is NOT VALID")
            return False
        
        logger.info(f"Schema is VALID")
        return True