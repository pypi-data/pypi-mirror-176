# -*- coding: utf-8 -*-
import pytest
from rich.table import Table

from moex.design import CliDesigner


@pytest.fixture
def table_empty():
    return CliDesigner.get_table()

@pytest.fixture
def table_with_headers():
    return CliDesigner.get_table("column1", "column2")

def test_empty_table(table_empty):
    assert isinstance(table_empty, Table)

def test_table_with_headers(table_with_headers):
    assert isinstance(table_with_headers, Table)
