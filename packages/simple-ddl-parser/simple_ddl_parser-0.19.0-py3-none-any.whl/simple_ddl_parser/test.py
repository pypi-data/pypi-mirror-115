from simple_ddl_parser import DDLParser

ddl = """
create table table2 (
    col1 integer not null,
    col2 integer not null,
    constraint pkey_1 primary key (col1, col2) not enforced
    );
"""
result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
