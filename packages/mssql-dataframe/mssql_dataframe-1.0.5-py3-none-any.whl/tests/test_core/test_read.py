import warnings

import pytest
import pandas as pd

from mssql_dataframe import connect
from mssql_dataframe.core import create, write, read


class package:
    def __init__(self, connection):
        self.connection = connection
        self.create = create.create(connection)
        self.write = write.write(connection, adjust_sql_objects=False)
        self.read = read.read(connection)

@pytest.fixture(scope="module")
def sql():
    db = connect.connect(database_name='tempdb', server_name='localhost')
    yield package(db)
    db.connection.close()


def test_select_input_errors(sql):

    table_name = '##test_select_input_errors'
    sql.create.table(table_name, columns={
            'ColumnA': 'TINYINT'
    })

    with pytest.raises(ValueError):
        sql.read.select(table_name, limit='1')

    with pytest.raises(ValueError):
        sql.read.select(table_name, order_column='A', order_direction=None)

    with pytest.raises(ValueError):
        sql.read.select(table_name, order_column='A', order_direction='a')    


def test_select(sql):

    # create table and insert sample data
    table_name = '##test_select'
    sql.create.table(table_name, columns={
            'ColumnA': 'TINYINT',
            'ColumnB': 'INT',
            'ColumnC': 'BIGINT',
            'ColumnD': 'DATETIME',
            'ColumnE': 'VARCHAR(10)'
    }, primary_key_column="ColumnA")

    input = pd.DataFrame({
        'ColumnA': [5,6,7],
        'ColumnB': [5,6,None],
        'ColumnC': [pd.NA,6,7],
        'ColumnD': ['06-22-2021','06-22-2021',pd.NaT],
        'ColumnE' : ['a','b',None]
    })
    input['ColumnB'] = input['ColumnB'].astype('Int64')
    input['ColumnD'] = pd.to_datetime(input['ColumnD'])
    sql.write.insert(table_name, input, include_timestamps=False)

    # all columns and rows
    dataframe = sql.read.select(table_name)
    assert dataframe.index.name=='ColumnA'
    assert dataframe.shape[1]==input.shape[1]-1
    assert dataframe.shape[0]==input.shape[0]
    assert dataframe.dtypes['ColumnB']=='Int32'
    assert dataframe.dtypes['ColumnC']=='Int64'
    assert dataframe.dtypes['ColumnD']=='datetime64[ns]'
    assert dataframe.dtypes['ColumnE']=='object'

    # optional columns specified
    dataframe = sql.read.select(table_name, column_names=["ColumnB","ColumnC"])
    assert dataframe.index.name=='ColumnA'
    assert all(dataframe.columns==["ColumnB","ColumnC"])
    assert dataframe.shape[0]==input.shape[0]

    # optional where statement
    dataframe = sql.read.select(table_name, column_names=['ColumnB','ColumnC','ColumnD'], where="ColumnB>4 AND ColumnC IS NOT NULL OR ColumnD IS NULL")
    assert sum((dataframe['ColumnB']>4 & dataframe['ColumnC'].notna()) | dataframe['ColumnD'].isna())==2

    # optional limit
    dataframe = sql.read.select(table_name, limit=1)
    assert dataframe.shape[0]==1

    # optional order
    dataframe = sql.read.select(table_name, column_names=["ColumnB"], order_column='ColumnA', order_direction='DESC')
    assert dataframe.index.name=='ColumnA'
    assert all(dataframe.index==[7,6,5])


def test_select_undefined_type(sql):

    table_name = '##test_select_undefined_type'
    columns = {"_geography": "GEOGRAPHY", "_datetimeoffset": "DATETIMEOFFSET(4)"}
    sql.create.table(table_name, columns)

    geography = "geography::STGeomFromText('LINESTRING(-122.360 47.656, -122.343 47.656)', 4326)"
    datetimeoffset = "'12-10-25 12:32:10 +01:00'"
    statement = "INSERT INTO {table_name} VALUES({geography},{datetimeoffset})"
    sql.connection.connection.cursor().execute(statement.format(
        table_name=table_name,
        geography=geography,
        datetimeoffset=datetimeoffset
    ))

    with warnings.catch_warnings(record=True) as warn:
        dataframe = sql.read.select(table_name)
        assert len(warn)==1
        assert issubclass(warn[-1].category, UserWarning)
        assert "['_geography', '_datetimeoffset']" in str(warn[-1].message)
        assert len(dataframe)==1
        assert all(dataframe.columns==['_geography', '_datetimeoffset'])