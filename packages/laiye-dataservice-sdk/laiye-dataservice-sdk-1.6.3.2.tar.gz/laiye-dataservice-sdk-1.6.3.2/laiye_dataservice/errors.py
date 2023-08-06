from .enums import AuthorizationType


class UnsupportedAuthorizationType(Exception):
    def __init__(self, auth_type):
        super().__init__(
            f"Unsupported authorization type {auth_type}, it just support " 
            f"[{AuthorizationType.UserCenter}, {AuthorizationType.BuiltInUser}, {AuthorizationType.JwtToken}]"
        )


class JwtTokenInfoTypeError(Exception):
    def __init__(self):
        super().__init__(f"Jwt token info just support dict or str type")


class GetBuiltinUserTokenFailedError(Exception):
    def __init__(self, code, error_code, msg):
        super().__init__(
            f"Get token error, please confirm your base_url, username or password. code=[{code}]"
            f", error_code=[{error_code}], msg=[{msg}]"
        )

