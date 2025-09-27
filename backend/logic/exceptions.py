class AppError(Exception):
    def __init__(self, message: str = "Base Application Error.", error_code: int = 400):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class InvalidCredentialsError(AppError):
    def __init__(self, message: str = "Password or e-mail is incorrect.", error_code: int = 400):
        super().__init__(message, error_code)


class InvalidEmailError(AppError):
    def __init__(self, message: str = "E-mail that you've given is inactive/unreachable/doesn't exist.", error_code: int = 400):
        super().__init__(message, error_code)


class UserAlreadyRegisteredError(AppError):
    def __init__(self, message: str = "Such e-mail has already been registered.", error_code: int = 400):
        super().__init__(message, error_code)


class UserNotFoundError(AppError):
    def __init__(self, message: str = "User not found.", error_code: int = 404):
        super().__init__(message, error_code)


class ChatNotFoundError(AppError):
    def __init__(self, message: str = "Chat not found.", error_code: int = 404):
        super().__init__(message, error_code)


class MemberNotFoundError(AppError):
    def __init__(self, message: str = "Member not found.", error_code: int = 404):
        super().__init__(message, error_code)

class MemberAlreadyExistsError(AppError):
    def __init__(self, message: str = "Member has already been added to this chat.", error_code: int = 400):
        super().__init__(message, error_code)


class MessageNotFoundError(AppError):
    def __init__(self, message: str = "Message not found.", error_code: int = 404):
        super().__init__(message, error_code)

class MemberRoleError(AppError):
    def __init__(self, message: str = "Your role in chat doesn't allow you to perform this action.", error_code: int = 401):
        super().__init__(message, error_code)
