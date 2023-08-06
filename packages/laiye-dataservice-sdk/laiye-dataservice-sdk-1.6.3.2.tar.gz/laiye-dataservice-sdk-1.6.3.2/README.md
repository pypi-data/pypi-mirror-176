这是来也[数据服务](https://cloud.laiye.com/dataservice)对应的SDK。

# Initialize a client ｜ 初始化客户端
```python
from laiye_dataservice import DataService, AuthorizationType, DSResult

client = DataService(
    "https://cloud.laiye.com/dataservice",
    'BuiltInUser',
    username="this is username",
    password="this is password",
    api_key=None,
    timeout_seconds=30,
    language='en'
)

result: DSResult = client.get_schema("schema_name")

print(result.get_data())
print(result.get_code())
print(result.get_message())
```
# Authorization | 权限相关
## logout
[退出登录](https://test-cloud.laiye.com/dataservice/doc.html#/v1.0/%E7%94%A8%E6%88%B7%E5%8F%8A%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86/logoutUsingGET)

`logout()`

**示例**
```python
result: DSResult = client.logout()
```

# Metadata Management | 元信息维护
## create_schema
[添加数据表](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E5%85%83%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86/addSchemaUsingPOST)

`create_schema(self, schema_api_name, display_name, description='') -> DSResult`
* schema_api_name: 数据表名称
* display_name: 数据表显示名称
* description: 描述信息，默认为空字符串

**示例**
```python
result: DSResult = self.ds.create_schema("test_01", "Test 01", "")
```

## delete_schema
[删除数据表](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E5%85%83%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86/deleteSchemaByIdUsingGET)

`delete_schema(self, schema_api_name, expansion_level=2) -> DSResult`
* schema_api_name: 数据表名称
* expansion_level: 数据展开层级，默认为2

## get_schemas
[获取数据表列表](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E5%85%83%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86/getSchemasUsingGET)

`get_schemas(self, start_id=0, limit=1000, order='asc', expansion_level=2) -> DSResult`
* start_id: 开始记录ID，默认值0。
* limit: 返回的最多记录数，默认值1000。
* order: 排序方式，默认为 'asc'， 也可以选择 'desc'
* expansion_level: 数据展开层级，默认为2

## get_schema
[获取数据表详情](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E5%85%83%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86/getSchemaUsingGET)

`get_schema(self, schema_api_name, expansion_level=2) -> DSResult`
* schema_api_name: 数据表名称
* expansion_level: 数据展开层级，默认为2

## add_fields
[添加字段-批量](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E5%85%83%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86/addSchemaFieldsUsingPOST)

`add_fields(self, schema_api_name, fields, expansion_level=2) -> DSResult`
* schema_api_name: 数据表名称
* fields: 字段数据，是一个字典数组
```python
[
  {
    "apiName": "",
    "displayName": "",
    "description": "",
    "dataMaxLength": 0,
    "dataMaxValue": 0,
    "dataMinLength": 0,
    "dataMinValue": 0,
    "defaultValue": "",
    "fieldType": "", # 字段类型,可用值:BOOLEAN,DATE,DATETIME,DOUBLE,FILE,HTML,IMAGE,JSON,LONG,MARKDOWN,RELATIONSHIP,TEXT,TIME
    "orderNum": 0,
    "pointLength": 0,
    "referenceDisplayFieldApiName": "",
    "referenceJoinFieldApiName": "",
    "referenceSchemaApiName": "",
    "allowNull": false,
  }
]
```
* expansion_level: 数据展开层级，默认为2

## delete_fields
[删除字段-批量](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E5%85%83%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86/deleteSchemaFieldsByApiNamesUsingPOST)
 
`delete_fields(self, schema_api_name, field_api_names, expansion_level=2) -> DSResult:`
 * schema_api_name: 数据表名称
 * field_api_names: 字段名称列表
 * expansion_level: 数据展开层级，默认为2

## add_index
[添加索引](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E5%85%83%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86/addSchemaIndexUsingPOST)

`add_index(self, schema_api_name, index, expansion_level=2) -> DSResult`
* schema_api_name: 数据表名称
* index: 要增加的索引描述
```python
{
  "apiName": "",
  "description": "",
  "displayName": "",
  "fieldApiNames": ['field1', 'field2'],
  "type": "UNIQUE" # 索引类型,可用值:GENERAL,UNIQUE
}
```
* expansion_level: 数据展开层级，默认为2

## get_index
[获取单个索引信息](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E5%85%83%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86/getSchemaIndexUsingGET)

`get_index(self, schema_api_name, index_api_name, expansion_level=2) -> DSResult`
* schema_api_name: 数据表名称
* index_api_name: 索引名称
* expansion_level: 数据展开层级，默认为2

# Data Management | 数据管理
## add_records
[新增实体(记录)](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/addEntityUsingPOST)

`add_record(self, schema_api_name, record, update_or_insert=False, response_with_data=False) -> DSResult`
* schema_api_name: 数据表名称
* record: 数据记录，是一个字典
```json
{"name": "Tom", "age":  20}
```
* update_or_insert: 如果数据存在是否将其替换，默认为 False。这个能力需要在数据表上先创建唯一索引。

## add_records
[新增实体(记录)-批量](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/addEntitiesUsingPOST)

`add_records(self, schema_api_name, records, update_or_insert=False, response_with_data=False) -> DSResult`
* schema_api_name: 数据表名称
* records: 数据记录，是一个字典数组
```json
[{"name": "Tom", "age":  20}, {"name": "Jack", "length":  180}]
```
* update_or_insert: 如果数据存在是否将其替换，默认为 False。这个能力需要在数据表上先创建唯一索引。

## delete_records 
[删除实体(记录)-批量](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/deleteEntitiesUsingPOST)

`def delete_records(self, schema_api_name, record_ids, response_with_data=False) -> DSResult:` 
* schema_api_name: 数据表名称
* record_ids: 记录ID列表
* response_with_data: 是否将操作的数据返回，默认为False。

## delete_record
[删除实体(记录)](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/deleteEntityUsingGET)

`delete_record(self, schema_api_name, record_id, response_with_data=False) -> DSResult:`
* schema_api_name: 数据表名称
* record_id: 记录ID
* response_with_data: 是否将操作的数据返回，默认为False。

## search_records
[查询实体(记录)列表-支持组合查询条件和组合排序条件](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/queryDataUsingPOST)

`search_records(self, schema_api_name, search_data) -> DSResult:`
* schema_api_name: 数据表名称
* search_data: 查询消息体

## get_records
[获取实体(记录)列表](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/getEntitiesUsingGET)

`get_records(self, schema_api_name, start_id=0, limit=1000, order='asc') -> DSResult`
* schema_api_name: 数据表名称
* start_id: 开始记录ID，默认值0。
* limit: 返回的最多记录数，默认值1000。
* order: 排序方式，默认为 'asc'， 也可以选择 'desc'

## update_records 
[更新实体(记录)-批量](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/updateEntitiesUsingPOST)

`update_records(self, schema_api_name, records, response_with_data=False) -> DSResult:` 
* schema_api_name: 数据表名称
* records: 要修改的记录列表，一个字典列表。
* response_with_data: 是否将操作的数据返回，默认为False。

## update_record 
[更新实体(记录)](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/updateEntityUsingPOST)

`update_record(self, schema_api_name, record_id, record, response_with_data=False) -> DSResult:`
* schema_api_name: 数据表名称
* record_id: 记录ID
* record: 要修改的记录，一个字典。
* response_with_data: 是否将操作的数据返回，默认为False。

## exec_select_sql 
[SQL执行](https://cloud.laiye.com/dataservice/doc.html#/v1.0/%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86/sqlExecuteUsingPOST)

`exec_select_sql(self, select_sql) -> DSResult:` 
* select_sql: SQL语句，字符串类型。