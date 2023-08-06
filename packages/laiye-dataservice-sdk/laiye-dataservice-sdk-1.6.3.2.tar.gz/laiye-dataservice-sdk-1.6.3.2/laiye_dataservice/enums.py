from enum import Enum, unique


class AuthorizationType(Enum):
    UserCenter = 1
    BuiltInUser = 2
    JwtToken = 3

    @staticmethod
    def analysis(item):
        if isinstance(item, AuthorizationType):
            return item
        else:
            return AuthorizationType[item]


class HttpMethod(Enum):
    GET = 'get'
    POST = 'post'

    @staticmethod
    def analysis(item):
        if isinstance(item, HttpMethod):
            return item
        else:
            return HttpMethod[item]


@unique
class Language(Enum):
    EN = 'en'
    zh_CN = 'zh-CN'

    @staticmethod
    def analysis(item):
        if isinstance(item, Language):
            return item
        else:
            return Language[item]
