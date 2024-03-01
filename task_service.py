
class TaskService:
    __func = None
    def __init__(self, func:callable):
        self.__func = func

    def exec(self, *args, **kwargs):
        """
        Executa a função personalizada com os argumentos fornecidos.
        """
        return self.__func(*args, **kwargs)