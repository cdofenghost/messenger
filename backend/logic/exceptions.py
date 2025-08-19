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