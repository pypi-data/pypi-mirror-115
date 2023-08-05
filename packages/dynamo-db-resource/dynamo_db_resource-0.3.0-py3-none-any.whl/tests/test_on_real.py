from dynamo_db_resource.dynamo_db_table import Table
from os import environ
from pathlib import Path

# environ["AWS_REGION"] = "eu-central-1"
# environ["DYNAMO_DB_RESOURCE_SCHEMA_ORIGIN"] = "file"
# environ["DYNAMO_DB_RESOURCE_SCHEMA_DIRECTORY"] = str(Path(__file__).parent) + "/test_data/tables/"
#

# def test_real():
#     t = Table("TableForInfrastructureTest", special_resource_config={"region_name": "eu-central-1"})
#     t.put(
#         {
#             "primary_partition_key": "second_key",
#             "some_string": "abc",
#             "some_string_set": {"a", "b"}
#         }
#     )
