from unittest import TestCase
from laiye_dataservice import JwtTokenInfo, DataService, AuthorizationType
from tests import local_data


class TestJwtToken(TestCase):
    @staticmethod
    def setUpClass() -> None:
        TestJwtToken.ds = DataService(
            local_data.get_base_url(),
            AuthorizationType.BuiltInUser,
            api_key=local_data.get_api_key()
        )

    def setUp(self) -> None:
        self.ds: DataService = TestJwtToken.ds

    def test_01_get_queries(self):
        result = self.ds.get_queries()
        self.assertEqual(result.get_code(), 200)
        self.assertTrue(len(result.get_data()) >= 1)

    def test_03_cached_query_result(self):
        result = self.ds.get_query_result(2913, if_refresh=False)
        self.assertEqual(result.get_code(), 200)
        self.assertTrue(len(result.get_data()['data']['rows']) > 0)

    def test_02_refresh_query_result(self):
        result = self.ds.get_query_result(2913, if_refresh=True)
        self.assertEqual(result.get_code(), 200)
        self.assertTrue(len(result.get_data()['data']['rows']) > 0)


