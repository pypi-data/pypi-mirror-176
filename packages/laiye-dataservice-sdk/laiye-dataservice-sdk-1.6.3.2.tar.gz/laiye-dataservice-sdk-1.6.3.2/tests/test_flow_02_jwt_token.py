from unittest import TestCase
from laiye_dataservice import JwtTokenInfo, DataService, AuthorizationType
from tests import local_data


class TestJwtToken(TestCase):
    @staticmethod
    def setUpClass() -> None:
        TestJwtToken.ds = DataService(
            local_data.get_base_url(),
            AuthorizationType.JwtToken,
            jwt_token_info=local_data.get_jwt_token_info()
        )

    def setUp(self) -> None:
        self.ds: DataService = TestJwtToken.ds

    def test_10_get_schemas(self):
        result = self.ds.get_schemas()
        self.assertEqual(result.get_code(), 200)
        self.assertTrue(len(result.get_data()) >= 1)
