

class ArgsErrorException(BaseException):

    def __init__(self, code=None, mes="", *args: object, **kwargs: object) -> None:
        self.code = code
        self.mes = mes
        super().__init__(*args, **kwargs)

