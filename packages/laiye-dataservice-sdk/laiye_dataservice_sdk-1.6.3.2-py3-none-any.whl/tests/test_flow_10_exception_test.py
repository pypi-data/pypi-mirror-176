from unittest import TestCase
from laiye_dataservice import DataService, DSResult, Language, AuthorizationType, GetBuiltinUserTokenFailedError
from tests import local_data
from uuid import uuid1


class TestJwtToken(TestCase):
    def test_01_error_builtin_user_info(self):
        self.assertRaises(
            GetBuiltinUserTokenFailedError,
            DataService,
            local_data.get_base_url(),
            AuthorizationType.BuiltInUser,
            username=str(uuid1()),
            password=str(uuid1()),
        )
