import duckdb
import os
import sys
try:
    import pyarrow as pa
    can_run = True
except:
    can_run = False

def numeric_operators(data_type):
        duckdb_conn = duckdb.connect()
        duckdb_conn.execute("CREATE TABLE test (a "+data_type+", b "+data_type+", c "+data_type+")")
        duckdb_conn.execute("INSERT INTO  test VALUES (1,1,1),(10,10,10),(100,10,100),(NULL,NULL,NULL)")
        duck_tbl = duckdb_conn.table("test")
        arrow_table = duck_tbl.arrow()
        print (arrow_table)

        duckdb_conn.register_arrow("testarrow",arrow_table)
        # Try ==
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a =1").fetchone()[0] == 1
        # Try >
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >1").fetchone()[0] == 2
        # Try >=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >=10").fetchone()[0] == 2
        # Try <
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <10").fetchone()[0] == 1
        # Try <=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <=10").fetchone()[0] == 2
        
        # Try Is Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NULL").fetchone()[0] == 1
        # Try Is Not Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NOT NULL").fetchone()[0] == 3
        
        # Try And
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a=10 and b =1").fetchone()[0] == 0
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a =100 and b = 10 and c = 100").fetchone()[0] == 1
        # Try Or
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a = 100 or b =1").fetchone()[0] == 2

class TestArrowFilterPushdown(object):
    def test_filter_pushdown_numeric(self,duckdb_cursor):
        if not can_run:
            return
        numeric_types = ['TINYINT', 'SMALLINT', 'INTEGER', 'BIGINT', 'UTINYINT', 'USMALLINT', 'UINTEGER', 'UBIGINT', 
        'FLOAT', 'DOUBLE']

        for data_type in numeric_types:
            numeric_operators(data_type)

# ArrowNotImplementedError: Function equal has no kernel matching input types (array[decimal128(4, 1)], scalar[decimal128(4, 1)])
    # def test_filter_pushdown_hugeint(self,duckdb_cursor):
    #     numeric_operators('HUGEINT')

    # def test_filter_pushdown_decimal(self,duckdb_cursor):
    #     numeric_types = ['DECIMAL(4,1)','DECIMAL(9,1)','DECIMAL(18,4)'],'DECIMAL(30,12)']

    #     for data_type in numeric_types:
    #         numeric_operators(data_type)

    def test_filter_pushdown_varchar(self,duckdb_cursor):
        if not can_run:
            return
        duckdb_conn = duckdb.connect()
        duckdb_conn.execute("CREATE TABLE test (a  VARCHAR, b VARCHAR, c VARCHAR)")
        duckdb_conn.execute("INSERT INTO  test VALUES ('1','1','1'),('10','10','10'),('100','10','100'),(NULL,NULL,NULL)")
        duck_tbl = duckdb_conn.table("test")
        arrow_table = duck_tbl.arrow()

        duckdb_conn.register_arrow("testarrow",arrow_table)
        # Try ==
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a ='1'").fetchone()[0] == 1
        # Try >
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >'1'").fetchone()[0] == 2
        # Try >=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >='10'").fetchone()[0] == 2
        # Try <
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <'10'").fetchone()[0] == 1
        # Try <=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <='10'").fetchone()[0] == 2
        
        # Try Is Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NULL").fetchone()[0] == 1
        # Try Is Not Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NOT NULL").fetchone()[0] == 3
        
        # Try And
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a='10' and b ='1'").fetchone()[0] == 0
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a ='100' and b = '10' and c = '100'").fetchone()[0] == 1
        # Try Or
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a = '100' or b ='1'").fetchone()[0] == 2

    def test_filter_pushdown_bool(self,duckdb_cursor):
        if not can_run:
            return
        duckdb_conn = duckdb.connect()
        duckdb_conn.execute("CREATE TABLE test (a  BOOL, b BOOL)")
        duckdb_conn.execute("INSERT INTO  test VALUES (TRUE,TRUE),(TRUE,FALSE),(FALSE,TRUE),(NULL,NULL)")
        duck_tbl = duckdb_conn.table("test")
        arrow_table = duck_tbl.arrow()

        duckdb_conn.register_arrow("testarrow",arrow_table)
        # Try ==
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a =True").fetchone()[0] == 2
        
        # Try Is Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NULL").fetchone()[0] == 1
        # Try Is Not Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NOT NULL").fetchone()[0] == 3
        
        # Try And
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a=True and b =True").fetchone()[0] == 1
        # Try Or
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a = True or b =True").fetchone()[0] == 3

    def test_filter_pushdown_time(self,duckdb_cursor):
        if not can_run:
            return
        duckdb_conn = duckdb.connect()
        duckdb_conn.execute("CREATE TABLE test (a  TIME, b TIME, c TIME)")
        duckdb_conn.execute("INSERT INTO  test VALUES ('00:01:00','00:01:00','00:01:00'),('00:10:00','00:10:00','00:10:00'),('01:00:00','00:10:00','01:00:00'),(NULL,NULL,NULL)")
        duck_tbl = duckdb_conn.table("test")
        arrow_table = duck_tbl.arrow()

        duckdb_conn.register_arrow("testarrow",arrow_table)
        # Try ==
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a ='00:01:00'").fetchone()[0] == 1
        # Try >
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >'00:01:00'").fetchone()[0] == 2
        # Try >=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >='00:10:00'").fetchone()[0] == 2
        # Try <
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <'00:10:00'").fetchone()[0] == 1
        # Try <=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <='00:10:00'").fetchone()[0] == 2
        
        # Try Is Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NULL").fetchone()[0] == 1
        # Try Is Not Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NOT NULL").fetchone()[0] == 3
        
        # Try And
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a='00:10:00' and b ='00:01:00'").fetchone()[0] == 0
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a ='01:00:00' and b = '00:10:00' and c = '01:00:00'").fetchone()[0] == 1
        # Try Or
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a = '01:00:00' or b ='00:01:00'").fetchone()[0] == 2

    def test_filter_pushdown_timestamp(self,duckdb_cursor):
        if not can_run:
            return
        duckdb_conn = duckdb.connect()
        duckdb_conn.execute("CREATE TABLE test (a  TIMESTAMP, b TIMESTAMP, c TIMESTAMP)")
        duckdb_conn.execute("INSERT INTO  test VALUES ('2008-01-01 00:00:01','2008-01-01 00:00:01','2008-01-01 00:00:01'),('2010-01-01 10:00:01','2010-01-01 10:00:01','2010-01-01 10:00:01'),('2020-03-01 10:00:01','2010-01-01 10:00:01','2020-03-01 10:00:01'),(NULL,NULL,NULL)")
        duck_tbl = duckdb_conn.table("test")
        arrow_table = duck_tbl.arrow()
        print (arrow_table)

        duckdb_conn.register_arrow("testarrow",arrow_table)
        # Try ==
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a ='2008-01-01 00:00:01'").fetchone()[0] == 1
        # Try >
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >'2008-01-01 00:00:01'").fetchone()[0] == 2
        # Try >=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >='2010-01-01 10:00:01'").fetchone()[0] == 2
        # Try <
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <'2010-01-01 10:00:01'").fetchone()[0] == 1
        # Try <=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <='2010-01-01 10:00:01'").fetchone()[0] == 2
        
        # Try Is Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NULL").fetchone()[0] == 1
        # Try Is Not Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NOT NULL").fetchone()[0] == 3
        
        # Try And
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a='2010-01-01 10:00:01' and b ='2008-01-01 00:00:01'").fetchone()[0] == 0
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a ='2020-03-01 10:00:01' and b = '2010-01-01 10:00:01' and c = '2020-03-01 10:00:01'").fetchone()[0] == 1
        # Try Or
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a = '2020-03-01 10:00:01' or b ='2008-01-01 00:00:01'").fetchone()[0] == 2
   
    def test_filter_pushdown_date(self,duckdb_cursor):
        if not can_run:
            return
        duckdb_conn = duckdb.connect()
        duckdb_conn.execute("CREATE TABLE test (a  DATE, b DATE, c DATE)")
        duckdb_conn.execute("INSERT INTO  test VALUES ('2000-01-01','2000-01-01','2000-01-01'),('2000-10-01','2000-10-01','2000-10-01'),('2010-01-01','2000-10-01','2010-01-01'),(NULL,NULL,NULL)")
        duck_tbl = duckdb_conn.table("test")
        arrow_table = duck_tbl.arrow()

        duckdb_conn.register_arrow("testarrow",arrow_table)
        # Try ==
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a ='2000-01-01'").fetchone()[0] == 1
        # Try >
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >'2000-01-01'").fetchone()[0] == 2
        # Try >=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a >='2000-10-01'").fetchone()[0] == 2
        # Try <
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <'2000-10-01'").fetchone()[0] == 1
        # Try <=
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a <='2000-10-01'").fetchone()[0] == 2
        
        # Try Is Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NULL").fetchone()[0] == 1
        # Try Is Not Null 
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a IS NOT NULL").fetchone()[0] == 3
        
        # Try And
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a='2000-10-01' and b ='2000-01-01'").fetchone()[0] == 0
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a ='2010-01-01' and b = '2000-10-01' and c = '2010-01-01'").fetchone()[0] == 1
        # Try Or
        assert duckdb_conn.execute("SELECT count(*) from testarrow where a = '2010-01-01' or b ='2000-01-01'").fetchone()[0] == 2
