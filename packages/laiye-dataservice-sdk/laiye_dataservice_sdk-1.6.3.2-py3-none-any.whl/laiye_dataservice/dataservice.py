import logging
import requests
import json
import time
from .enums import AuthorizationType, HttpMethod, Language
from .errors import UnsupportedAuthorizationType, GetBuiltinUserTokenFailedError
from .do import DSResult, JwtTokenInfo

logger = logging.getLogger(__name__)


class DataService:
    def __init__(
            self,
            base_url,
            auth_type=AuthorizationType.UserCenter,
            username=None,
            password=None,
            api_key=None,
            timeout_seconds=30,
            language=Language.EN,
            jwt_token_info=None,
            api_version='v1'
    ):
        self.base_url = DataService._normalize_base_url(base_url)
        self.auth_type = AuthorizationType.analysis(auth_type)
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.language = Language.analysis(language)
        self.access_token = None
        self.authorization = None
        self.token = None
        self.jwt_token = None
        self.api_version = api_version

        self.default_header = {"Content-Type": "application/json; charset=utf-8"}

        if self.auth_type == AuthorizationType.UserCenter:
            pass
        elif self.auth_type == AuthorizationType.BuiltInUser:
            self.token = self._get_token_of_builtin_user(username, password)
        elif self.auth_type == AuthorizationType.JwtToken:
            self.jwt_token = JwtTokenInfo.analysis(jwt_token_info).get_token()
        else:
            raise UnsupportedAuthorizationType(self.auth_type)

    def _get_authorized_header(self, api_url: str):
        header = self.default_header.copy()

        if self.auth_type == AuthorizationType.UserCenter:
            pass
        elif self.auth_type == AuthorizationType.BuiltInUser:
            header["Authorization"] = self.token
            if self._is_bi_request(api_url):
                header["Authorization"] = f'Key {self.api_key}'
        elif self.auth_type == AuthorizationType.JwtToken:
            header["Jwt-Token"] = self.jwt_token
        else:
            raise UnsupportedAuthorizationType(self.auth_type)

        return header

    def _query(self, http_method, api_url, data=None, if_need_auth=True):
        if if_need_auth:
            header = self._get_authorized_header(api_url)
        else:
            header = self.default_header.copy()

        header["Accept-Language"] = self.language.value

        if http_method == HttpMethod.GET:
            response = requests.get(
                api_url,
                headers=header,
                timeout=self.timeout_seconds
            )
        elif http_method == HttpMethod.POST:
            response = requests.post(
                api_url,
                headers=header,
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                timeout=self.timeout_seconds
            )
        else:
            logger.error(f"unsupported request method {http_method}")
            raise Exception(f"unsupported request method {http_method}")

        return response

    @staticmethod
    def _resolve_response(
            res, if_log_error_when_not_200=True, if_resolve_json_body_when_not_200=False, url=''
    ) -> DSResult:
        if res is None:
            logger.error("Response is none")
            raise Exception("Response is none")

        if res.status_code != 200 and if_log_error_when_not_200:
            logger.error(f'Request to [{url}] failed, res status [{res.status_code}], res content [{res.text}]')

        if res.status_code == 200 or if_resolve_json_body_when_not_200:
            data = res.json()
            return DSResult(data)

        return DSResult({"code": res.status_code, "errorCode": 0, "successfully": False})

    @staticmethod
    def _resolve_bi_response(
            res, if_log_error_when_not_200=True, if_resolve_json_body_when_not_200=False, url='', if_single_result=False
    ) -> DSResult:
        result = {'code': 200, 'amount': 0, 'message': '', 'data': None, 'errorCode': 0, 'page_size': 0, 'successfully': True}
        if res is None:
            logger.error("Response is none")
            raise Exception("Response is none")

        result['code'] = res.status_code
        if res.status_code != 200 and if_log_error_when_not_200:
            logger.error(f'Request to [{url}] failed, res status [{res.status_code}], res content [{res.text}]')

        if (res.status_code == 200 or if_resolve_json_body_when_not_200) and (not if_single_result):
            data = res.json()
            result['amount'] = data.get('count', 0)
            result['message'] = data.get('message', '')
            result['data'] = data.get('results')
            result['errorCode'] = data.get('errorCode', 0)
            result['page_size'] = data.get('page_size', 0)
            result['successfully'] = data.get('successfully', True)
        elif (res.status_code == 200 or if_resolve_json_body_when_not_200) and if_single_result:
            data = res.json()
            result['amount'] = 0
            result['message'] = ''
            result['data'] = data.get('query_result', data.get('job', data))
            result['errorCode'] = 0
            result['page_size'] = 0
            result['successfully'] = True
        else:
            raise Exception("unhandled branch")

        return DSResult(result)

    def _get_data_table_url(self, api_url):
        if api_url.startswith("/"):
            return f"{self.base_url}/api/{self.api_version}{api_url}"
        return f"{self.base_url}/api/{self.api_version}/{api_url}"

    def _get_bi_url(self, api_url):
        if api_url.startswith("/"):
            return f"{self.base_url}/bi{api_url}"
        return f"{self.base_url}/bi/{api_url}"

    def _is_bi_request(self, url: str):
        api_path = url.replace(self.base_url, "")
        return api_path.startswith("/bi")

    @staticmethod
    def _normalize_base_url(url: str):
        url = url.strip()
        if url[-1] != '/':
            return url
        return url[0:-1]

    def _get_token_of_builtin_user(self, username, password):
        if self.api_key is not None and username is None:
            return None

        result = self.get_auth_token(username, password)
        if result.get_code() != 200 or result.get_data() is None:
            raise GetBuiltinUserTokenFailedError(result.get_code(), result.get_error_code(), result.get_message())

        return result.get_data().get('token')

    """Auth"""
    def get_auth_token(self, username, password) -> DSResult:
        url = self._get_data_table_url(f'/user/auth')
        res = self._query(HttpMethod.POST, url, data={"username": username, "password": password}, if_need_auth=False)
        result = self._resolve_response(res, if_log_error_when_not_200=True, url=url)
        if result.get_code() != 200:
            logger.warning(
                f'get auth token error, message=[{result.get_message()}], status_code=[{result.get_code()}],'
                f' error_code={result.get_error_code()}'
            )
        return result

    def logout(self):
        url = self._get_data_table_url(f'/user/logout')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def who_am_i(self):
        url = self._get_data_table_url(f'/user/whoami')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    """ Schema """
    def create_schema(self, api_name, display_name, description='') -> DSResult:
        url = self._get_data_table_url(f'/ddl/schema/add')
        data = {
            "apiName": api_name,
            "description": description,
            "displayName": display_name,
            "etag": 0,
            "ifEnableCls": False,
            "ifEnableRls": False
        }
        res = self._query(HttpMethod.POST, url, data=data)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def delete_schema(self, schema_api_name, expansion_level=2) -> DSResult:
        url = self._get_data_table_url(f'/ddl/schema/delete/{schema_api_name}?expansionLevel={expansion_level}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def get_schemas(self, start_id=0, limit=1000, order='asc', expansion_level=2) -> DSResult:
        url = self._get_data_table_url(f'/ddl/schema/read/?startId={start_id}&limit={limit}&order={order}&expansionLevel={expansion_level}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def get_schema(self, schema_api_name, expansion_level=2) -> DSResult:
        url = self._get_data_table_url(f'/ddl/schema/read/{schema_api_name}?expansionLevel={expansion_level}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def add_fields(self, schema_api_name, fields, expansion_level=2) -> DSResult:
        url = self._get_data_table_url(f'/ddl/schema/{schema_api_name}/field/add?expansionLevel={expansion_level}')
        res = self._query(HttpMethod.POST, url, data=fields)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def delete_fields(self, schema_api_name, field_api_names, expansion_level=2) -> DSResult:
        url = self._get_data_table_url(f'/ddl/schema/{schema_api_name}/field/delete?expansionLevel={expansion_level}')
        res = self._query(HttpMethod.POST, url, data=field_api_names)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def add_index(self, schema_api_name, index, expansion_level=2) -> DSResult:
        url = self._get_data_table_url(f'/ddl/schema/{schema_api_name}/index/add?expansionLevel={expansion_level}')
        res = self._query(HttpMethod.POST, url, data=index)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def get_index(self, schema_api_name, index_api_name, expansion_level=2) -> DSResult:
        url = self._get_data_table_url(f'/ddl/schema/{schema_api_name}/index/read/{index_api_name}?expansionLevel={expansion_level}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    """ Data """

    def add_record(self, schema_api_name, record, update_or_insert=False, response_with_data=False) -> DSResult:
        url = self._get_data_table_url(f'/dml/entity/{schema_api_name}/add?upsert={update_or_insert}&responseWithData={response_with_data}')
        res = self._query(HttpMethod.POST, url, data=record)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def add_records(self, schema_api_name, records, update_or_insert=False, response_with_data=False) -> DSResult:
        url = self._get_data_table_url(f'/dml/entity/{schema_api_name}/add-batch?upsert={update_or_insert}&responseWithData={response_with_data}')
        res = self._query(HttpMethod.POST, url, data=records)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def delete_records(self, schema_api_name, record_ids, response_with_data=False) -> DSResult:
        url = self._get_data_table_url(f'/dml/entity/{schema_api_name}/delete-batch?responseWithData={response_with_data}')
        res = self._query(HttpMethod.POST, url, data=record_ids)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def delete_record(self, schema_api_name, record_id, response_with_data=False) -> DSResult:
        url = self._get_data_table_url(f'/dml/entity/{schema_api_name}/delete/{record_id}?responseWithData={response_with_data}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def search_records(self, schema_api_name, search_data) -> DSResult:
        url = self._get_data_table_url(f'/dml/entity/{schema_api_name}/query-data')
        res = self._query(HttpMethod.POST, url, data=search_data)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def get_records(self, schema_api_name, start_id=0, limit=1000, order='asc') -> DSResult:
        url = self._get_data_table_url(f'/dml/entity/{schema_api_name}/read?startId={start_id}&limit={limit}&order={order}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def update_records(self, schema_api_name, records, response_with_data=False) -> DSResult:
        url = self._get_data_table_url(f'/dml/entity/{schema_api_name}/update-batch?responseWithData={response_with_data}')
        res = self._query(HttpMethod.POST, url, data=records)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def update_record(self, schema_api_name, record_id, record, response_with_data=False) -> DSResult:
        url = self._get_data_table_url(f'/dml/entity/{schema_api_name}/update/{record_id}?responseWithData={response_with_data}')
        res = self._query(HttpMethod.POST, url, data=record)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def exec_select_sql(self, select_sql) -> DSResult:
        url = self._get_data_table_url(f'/dml/sql/execute')
        res = self._query(HttpMethod.POST, url, data={"query": select_sql})
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    """BI"""
    def get_queries(self, page=1, page_size=20, order='created_at'):
        url = self._get_bi_url(f'/api/queries?order={order}&page={page}&page_size={page_size}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_bi_response(res, if_log_error_when_not_200=True, url=url)

    def get_query(self, query_id):
        url = self._get_bi_url(f'/api/queries/{query_id}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_bi_response(res, if_log_error_when_not_200=True, url=url, if_single_result=True)

    def exec_query(self, query_id, params={}):
        url = self._get_bi_url(f'/api/queries/{query_id}/results')
        res = self._query(
            HttpMethod.POST,
            url,
            {"apply_auto_limit": False, "id": query_id, "max_age": 0, "parameters": params}
        )
        return self._resolve_bi_response(res, if_log_error_when_not_200=True, url=url, if_single_result=True)

    def get_job_status(self, job_id):
        url = self._get_bi_url(f'/api/jobs/{job_id}')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_bi_response(res, if_log_error_when_not_200=True, url=url, if_single_result=True)

    def get_cached_query_result(self, query_id, result_id):
        url = self._get_bi_url(f'/api/queries/{query_id}/results/{result_id}.json')
        res = self._query(HttpMethod.GET, url)
        return self._resolve_bi_response(res, if_log_error_when_not_200=True, url=url, if_single_result=True)

    def get_query_result(self, query_id, params={}, if_refresh=False, time_seconds=30):
        result_id = 0
        if not if_refresh:
            query_info = self.get_query(query_id)
            result_id = query_info.get_data().get('latest_query_data_id')
        else:
            job_info = self.exec_query(query_id, params)
            job_id = job_info.get_data().get('id')
            for _ in range(int(time_seconds)):
                job_info = self.get_job_status(job_id)
                if job_info.get_data()['status'] == 3:
                    result_id = job_info.get_data()['query_result_id']
                    break
                time.sleep(1)

        return self.get_cached_query_result(query_id, result_id)
