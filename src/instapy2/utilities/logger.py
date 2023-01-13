from logging import DEBUG, Formatter, getLogger, StreamHandler

class Logger:
    def __errorHandler(self) -> StreamHandler:
        handler = StreamHandler()
        handler.setFormatter(fmt=self.formatter)
        handler.setLevel(level=DEBUG)

        return handler

    def __infoHandler(self) -> StreamHandler:
        handler = StreamHandler()
        handler.setFormatter(fmt=self.formatter)
        handler.setLevel(level=DEBUG)

        return handler
    

    def __init__(self):
        self.formatter = Formatter(fmt='[%(levelname)s]: %(message)s')
        
        self.error_logger = getLogger(name='error')
        self.error_logger.addHandler(hdlr=self.__errorHandler())

        self.info_logger = getLogger(name='info')
        self.info_logger.addHandler(hdlr=self.__infoHandler())

    
    def error(self, message: str):
        self.error_logger.error(msg=message)

    def info(self, message: str):
        self.info_logger.info(msg=message)