from unittest import TestCase
from laiye_dataservice import DataService, DSResult, Language
from tests import local_data
import time
import uuid


class BuiltInLoginTest(TestCase):

    def setUp(self) -> None:
        self.schema_name = BuiltInLoginTest.schema_name
        self.ds: DataService = BuiltInLoginTest.ds

    @staticmethod
    def setUpClass() -> None:
        BuiltInLoginTest.schema_name = 'dataservice_sdk_test'
        BuiltInLoginTest.ds = DataService(
            local_data.get_base_url(),
            local_data.get_auth_type(),
            username=local_data.get_username(),
            password=local_data.get_password(),
        )

    @staticmethod
    def tearDownClass() -> None:
        result: DSResult = BuiltInLoginTest.ds.get_schema(BuiltInLoginTest.schema_name)
        if result.get_code() != 200:
            return
        BuiltInLoginTest.ds.delete_schema(result.get_data().get("apiName"))
        BuiltInLoginTest.ds.logout()

    def test_00000_auth(self):
        ds = DataService(
            local_data.get_base_url(),
            'BuiltInUser',
            username=local_data.get_username(),
            password=local_data.get_password(),
        )

        result: DSResult = ds.get_schemas()
        self.assertEqual(result.get_code(), 200)
        self.assertTrue(len(result.get_data()) > 0)

        result: DSResult = ds.get_schema(uuid.uuid1())
        self.assertTrue(result.get_message().find('does not exist') > 0)

        ds.language = Language.zh_CN
        result: DSResult = ds.get_schema(uuid.uuid1())
        self.assertTrue(result.get_message().find('不存在') > 0)

        result: DSResult = ds.who_am_i()
        self.assertEqual(result.get_code(), 200)
        self.assertEqual(result.get_data().get('username'), local_data.get_username())

    def test_00001_create_schema(self):
        result: DSResult = self.ds.create_schema(self.schema_name, self.schema_name, "")
        self.assertEqual(result.get_code(), 200)
        self.assertEqual(result.code, 200)
        self.assertEqual(result.get_data().get('apiName'), self.schema_name)
        self.assertIsNone(result.get_error_code())
        self.assertIsNotNone(result.get_message())
        self.assertIsNotNone(result.get_page_size())
        self.assertTrue(result.is_successfully())
        self.assertIsNotNone(result.get_json_data())

    def test_00010_add_fields(self):
        result: DSResult = self.ds.add_fields(
            self.schema_name,
            [
                {"allowNull": False, "apiName": "name", "dataMaxLength": 64, "dataMinLength": 2, "displayName": "name", "fieldType": "TEXT"},
                {"allowNull": False, "apiName": "address", "dataMaxLength": 64, "dataMinLength": 2, "displayName": "address", "fieldType": "TEXT"},
                {"allowNull": False, "apiName": "age", "displayName": "age", "fieldType": "LONG"}
            ]
        )

        self.assertEqual(result.get_code(), 200)
        self.assertEqual(len(result.get_data()), 3)

    def test_00020_add_fields(self):
        result: DSResult = self.ds.delete_fields(self.schema_name, ['address'])
        self.assertEqual(result.get_code(), 200)
        self.assertEqual(len(result.get_data()), 1)

    def test_00030_add_index(self):
        result: DSResult = self.ds.add_index(self.schema_name, {
          "apiName": "test_index",
          "displayName": "test_index",
          "fieldApiNames": ["name"],
          "type": "UNIQUE"
        })
        self.assertEqual(result.get_code(), 200)

        for _ in range(6):
            result: DSResult = self.ds.get_index(self.schema_name, 'test_index')
            self.assertEqual(result.get_code(), 200)
            if result.get_data().get('status') == 'SUCCESSFUL':
                break
            time.sleep(1)

    def test_00050_add_records(self):
        result: DSResult = self.ds.add_records(self.schema_name, [
            {"name": "Tom", "age": 100},
            {"name": "Jack", "age": 99},
        ], update_or_insert=True)

        self.assertEqual(result.get_code(), 200)

        result: DSResult = self.ds.add_record(self.schema_name, {"name": "Golf", "age": 90}, update_or_insert=True)

        self.assertEqual(result.get_code(), 200)

        result: DSResult = self.ds.get_records(self.schema_name)
        self.assertEqual(result.get_code(), 200)
        self.assertEqual(result.get_amount(), 3)

    def test_00060_exec_query_and_update(self):
        result: DSResult = self.ds.search_records(self.schema_name, {
            "filterConditions": [{"parameters": [0], "fieldApiName": "id", "operator": "GT"}],
            "sortConditions": [{"fieldApiName": "name", "sortType": "desc"}]
        })

        record_1 = result.get_data()[0]
        record_1["name"] = "Tom1"
        result1: DSResult = self.ds.update_record(self.schema_name, record_1.get('id'), record_1, response_with_data=True)

        record_2 = result.get_data()[1]
        record_2['name'] = 'Jack1'
        result2: DSResult = self.ds.update_records(self.schema_name, [record_2])

        result: DSResult = self.ds.exec_select_sql(f"select * from {self.schema_name} order by name desc")
        self.assertEqual(len(result.get_data().get("rows")), 3)

        self.assertEqual(result.get_data().get('rows')[0].get('name'), 'Tom1')
        self.assertEqual(result.get_data().get('rows')[1].get('name'), 'Jack1')

    def test_00070_delete_records(self):
        result: DSResult = self.ds.get_records(self.schema_name)

        ids = [record.get('id') for record in result.get_data()]

        result: DSResult = self.ds.delete_record(self.schema_name, ids[0])
        self.assertEqual(result.get_code(), 200)

        result: DSResult = self.ds.delete_records(self.schema_name, ids[1:])
        self.assertEqual(result.get_code(), 200)

        result: DSResult = self.ds.get_records(self.schema_name)
        self.assertEqual(result.get_amount(), 0)

