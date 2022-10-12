class ControllerException(Exception):
    def __init__(self, message: str) -> None:
        super(ControllerException, self).__init__(message)
        self.message = message

class AlreadyExistException(ControllerException):
    def __init__(self, message: str) -> None:
        super(AlreadyExistException, self).__init__(message)

class NotFoundException(ControllerException):
    def __init__(self, message: str) -> None:
        super(NotFoundException, self).__init__(message)

class DataConflictException(ControllerException):
    def __init__(self, message: str) -> None:
        super(DataConflictException, self).__init__(message)

class NotAvailableException(ControllerException):
    def __init__(self, message: str) -> None:
        super(NotAvailableException, self).__init__(message)

class NotValidException(ControllerException):
    def __init__(self, message: str) -> None:
        super(NotValidException, self).__init__(message)
        