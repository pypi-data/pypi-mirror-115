from simple_ddl_parser import DDLParser

ddl = """

 CREATE TABLE foo.bar(
     asdf INTEGER ENCODE ZSTD NOT NULL,
     qwerty VARCHAR(255) ENCODE LZO
 )
COMPOUND
SORTKEY (qwerty)
 DISTSTYLE EVEN
 ;
"""
result = DDLParser(ddl).run(group_by_type=True, output_mode="redshift")
import pprint

pprint.pprint(result)
