# -*- coding: utf-8 -*-
from xml.etree import ElementTree

import pytest
from pandas import DataFrame

from moex.data_classes import JSON, XML, HTML


@pytest.fixture
def json_empty():
    return JSON(raw={})

@pytest.fixture
def json_not_empty():
    return JSON(raw={"some_key": {"columns": ["some_column"], "data": [["some_value"]]}})

@pytest.fixture
def xml_empty():
    return XML(raw=None)

@pytest.fixture
def xml_not_empty():
    return XML(raw="<root>\n<child>some text</child>\n</root>")

@pytest.fixture
def html_empty():
    return HTML(raw=None)

@pytest.fixture
def html_not_empty():
    return HTML(raw=""" <table>
  <tr>
    <th>Column 1</th>
    <th>Column 2</th>
    <th>Column 3</th>
  </tr>
  <tr>
    <td>Value 1</td>
    <td>Value 2</td>
    <td>Value 3</td>
  </tr>
</table> """)


def test_json_empty_to_df(json_empty):
    assert json_empty.to_df() is None
    assert json_empty.to_df("some_key") is None

def test_json_not_empty_to_df(json_not_empty):
    assert isinstance(json_not_empty.to_df(), DataFrame)
    assert json_not_empty.to_df("some_key_not_exists") is None

def test_xml_empty_to_tree(xml_empty):
    assert xml_empty.to_tree() is None

def test_xml_not_empty_to_tree(xml_not_empty):
    assert isinstance(xml_not_empty.to_tree(), ElementTree.Element)

def test_html_empty_to_df(html_empty):
    assert html_empty.to_df() is None

def test_html_not_empty_to_df(html_not_empty):
    assert isinstance(html_not_empty.to_df(), DataFrame)
