import json
from .jwt import encode as encode_jwt
from .errors import JwtTokenInfoTypeError


class JwtTokenInfo:
    def __init__(self, company_id: int, employee_id: int, company_name: str, employee_name: str, secret: str):
        self.company_id = company_id
        self.employee_id = employee_id
        self.company_name = company_name
        self.employee_name = employee_name
        self.secret = secret

    def get_token(self):
        return encode_jwt(
            {
                "CompanyId": str(self.company_id),
                "EmployeeId": str(self.employee_id),
                "CompanyName": self.company_name,
                "EmployeeName": self.employee_name,
            },
            self.secret,
            algorithm="HS256"
        )

    @staticmethod
    def analysis(item):
        if item is None:
            return None
        elif isinstance(item, JwtTokenInfo):
            return item
        elif isinstance(item, dict):
            json_data = item
        elif isinstance(item, str):
            json_data = json.loads(item)
        else:
            raise JwtTokenInfoTypeError()

        return JwtTokenInfo(**json_data)


class DSResult:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_amount(self):
        return self.json_data.get("amount")

    def get_code(self):
        return self.json_data.get("code")

    def get_data(self):
        return self.json_data.get('data')

    def get_error_code(self):
        return self.json_data.get('errorCode')

    def get_message(self):
        return self.json_data.get('message')

    def get_page_size(self):
        return self.json_data.get('page_size')

    def is_successfully(self):
        return self.json_data.get('successfully', False)

    def get_json_data(self):
        return self.json_data

    def __getattr__(self, item):
        return self.json_data.get(item)
