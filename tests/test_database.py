from numpy import outer
import pytest
import shutil
import os

from sqlite_integrated import *


@pytest.fixture
def db() -> Database:
    shutil.copy("tests/test.db", "tests/temp.db")
    yield Database("tests/temp.db", silent=True)
    os.remove("tests/temp.db")

def test_creating_database():
    with pytest.raises(DatabaseException):
        Database("does_not_exist.db")

def test_get_table_names(db):
    assert len(db.get_table_names()) == 13

def test_is_table(db):
    assert db.is_table(db.get_table_names()[0])

def test_get_table_raw(db):
    table_name = db.get_table_names()[1]
    table = db.get_table_raw(table_name)

    assert isinstance(table, list)
    assert isinstance(table[0], tuple)

def test_get_table_raw_and_get_table_columns(db):
    for table_name in db.get_table_names():
        table = db.get_table_raw(table_name)
        assert len(table[0]) == len(db.get_table_columns(table_name))

def test_get_table(db):
    table_name = "customers"
    raw_table = db.get_table_raw(table_name)
    table = db.get_table(table_name, id_field="CustomerId")

    assert len(raw_table) == len(table)
    assert isinstance(table, list)
    assert isinstance(table[0], DatabaseEntry)
    assert table[0].table == table_name

def test_null_fill(db):
    table_name = "customers"
    entry = DatabaseEntry({"FirstName": "TestName"}, table_name, None)
    filled_entry = db.fill_null(entry)

    assert len(filled_entry) == len(db.get_table(table_name)[0])

def test_get_entry_by_id(db):
    table_name = "customers"
    entry_by_id = db.get_entry_by_id(table_name, 1, id_field="CustomerId")
    entry_by_table = DatabaseEntry(db.get_table(table_name)[0], table_name, "CustomerId")

    assert len(entry_by_id) == len(entry_by_table)
    assert entry_by_id == entry_by_table

def test_add_table_entry(db):
    table_name = "customers"
    entry = DatabaseEntry({"FirstName": "TestFirstName", "LastName": "TestLastName", "Email": "TestEmail"}, table_name, None)

    before_table = db.get_table(table_name)
    db.add_table_entry(entry, fill_null=True)
    after_table = db.get_table(table_name)

    assert len(after_table) == len(before_table) + 1
    assert entry['FirstName'] == after_table[-1]['FirstName']


def test_update_entry(db):
    entry = db.get_entry_by_id("customers", 1, id_field="CustomerId")
    entry['FirstName'] = "TestName"
    db.update_entry(entry)

    entry_from_table = db.get_table("customers")[0]

    assert entry_from_table['FirstName'] == "TestName"
    assert entry == entry_from_table

def test_save(db):
    path = "tests/test_save.db"
    shutil.copy(db.path,path)

    db1 = Database(path)
    db2 = Database(db.path)

    assert db1 == db2

    entry = db1.get_entry_by_id("customers", 1, id_field="CustomerId")
    entry['FirstName'] = "Different Name"
    db1.update_entry(entry)

    assert db1 != db2

    db1.close()

    db3 = Database(path)

    assert db3 != db2

    with pytest.raises(sqlite3.ProgrammingError):
        assert db1 != db2
    
    db1.reconnect()
    assert db1 == db3

    os.remove(path)

def test_select(db):
    table_name = "customers"

    q = db.SELECT().FROM(table_name)

    table = db.get_table(table_name)
    
    assert q.run() == table
    assert q.run(raw = True) == db.get_table_raw(table_name)

    assert table[0] == db.SELECT().FROM(table_name).WHERE("CustomerId", 1).run()[0]
    assert table[0] == db.SELECT().FROM(table_name).WHERE("CustomerId = 1").run()[0]
    
    assert len(db.SELECT(["FirstName", "LastName"]).FROM("customers").run()[0]) == 2
    assert len(db.SELECT(["FirstName", "LastName"]).FROM("customers").WHERE("CustomerId", 1).run()[0]) == 2

def test_update(db):
    db1 = Database(db.path)
    db2 = Database(db.path)

    assert db1 == db2

    db1.UPDATE("customers").SET({"FirstName": "TestName"}).WHERE("CustomerId", 1).run()

    assert db1 != db2

    db1.close()

    db2.update_entry(db2.get_entry_by_id("customers", 1, id_field="CustomerId"))

    db1.reconnect()

    assert db1 == db2

def test_insert_into(db):
    db1 = Database(db.path)
    db2 = Database(db.path)

    assert db1 == db2

    data = {"FirstName": "TestFirst", "LastName": "TestLast", "Email": "test@mail.com"}

    table_name = "customers"

    db1.INSERT_INTO(table_name).VALUES(data).run()

    assert len(db1.get_table(table_name)) == len(db2.get_table(table_name)) + 1

    inserted_entry = db1.get_table(table_name)[-1]

    assert inserted_entry['Email'] == data['Email']
    assert inserted_entry['LastName'] == data['LastName']
    assert inserted_entry['FirstName'] == data['FirstName']

def test_export_to_csv(db):
    out_dir = "tests/test_export_to_csv"
    os.mkdir(out_dir)

    db.export_to_csv(out_dir, ["customers", "artists"])

    assert len(os.listdir(out_dir)) == 2

    db.export_to_csv(out_dir)

    assert len(os.listdir(out_dir)) == len(db.get_table_names())
    
    db.export_to_csv(out_dir, sep = ",")

    assert len(os.listdir(out_dir)) == len(db.get_table_names())

    # cleanup
    shutil.rmtree(out_dir)

def test_dataframe_to_table(db):
    df = db.table_to_dataframe("customers")

    name = "test_table"

    db.dataframe_to_table(name, df)

    assert db.get_table_names()[-1] == name

    
