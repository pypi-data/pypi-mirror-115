from simple_ddl_parser import DDLParser

ddl = """
 CREATE TABLE mydataset.newtable ( x INT64 )
"""
result = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
import pprint

pprint.pprint(result)
