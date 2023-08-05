# -*- coding: utf-8 -*-
import pytest
from bs4 import BeautifulSoup

from moex.handlers import (
    JSONHandler, XMLHandler, CSVHandler, HTMLHandler, Handlers, AVAILABLE
    )
from moex.exceptions import HandlersSearchError
from moex.tests_fixtures import client_session


@pytest.fixture
def handlers():
    handlers = Handlers()
    for handler in AVAILABLE:
        handlers.register(handler.EXTENSION, handler)
    return handlers

@pytest.fixture
def json_handler(): return JSONHandler()

@pytest.fixture
def xml_handler(): return XMLHandler()

@pytest.fixture
def csv_handler(): return CSVHandler()

@pytest.fixture
def html_handler(): return HTMLHandler()

@pytest.fixture
def url(): return "https://iss.moex.com/iss/securities/IMOEX"

@pytest.fixture
def bad_url(): return "https://iss.moex.com/iss/some/value"

@pytest.mark.asyncio
async def test_json_handler(client_session, json_handler, url):
    data = await json_handler.execute(client_session, url)
    assert data.raw is not None

@pytest.mark.asyncio
async def test_json_handler_bad_url(client_session, json_handler, bad_url):
    data = await json_handler.execute(client_session, bad_url)
    assert data.raw is None

@pytest.mark.asyncio
async def test_xml_handler(client_session, xml_handler, url):
    data = await xml_handler.execute(client_session, url)
    assert data.raw is not None

@pytest.mark.asyncio
async def test_xml_handler_bad_url(client_session, xml_handler, bad_url):
    data = await xml_handler.execute(client_session, bad_url)
    assert data.raw is None

@pytest.mark.asyncio
async def test_csv_handler(client_session, csv_handler, url):
    data = await csv_handler.execute(client_session, url)
    assert data.raw is not None

@pytest.mark.asyncio
async def test_csv_handler_bad_url(client_session, csv_handler, bad_url):
    data = await csv_handler.execute(client_session, bad_url)
    assert data.raw is None

@pytest.mark.asyncio
async def test_html_handler(client_session, html_handler, url):
    data = await html_handler.execute(client_session, url)
    assert data.raw is not None

@pytest.mark.asyncio
async def test_html_handler_bad_url(client_session, html_handler, bad_url):
    data = await html_handler.execute(client_session, bad_url)
    error_text = BeautifulSoup(data.raw, "html.parser").find_all("p")[0].text
    assert error_text == "Возможно, страница устарела, была удалена или перенесена на новый адрес."

def test_handlers_get_json(handlers):
    handler = handlers.create(output_format=".json")
    assert isinstance(handler, JSONHandler)

def test_handlers_get_xml(handlers):
    handler = handlers.create(output_format=".xml")
    assert isinstance(handler, XMLHandler)

def test_handlers_get_csv(handlers):
    handler = handlers.create(output_format=".csv")
    assert isinstance(handler, CSVHandler)

def test_handlers_get_html(handlers):
    handler = handlers.create(output_format=".html")
    assert isinstance(handler, HTMLHandler)

def test_handlers_get_some(handlers):
    with pytest.raises(HandlersSearchError):
        handlers.create(output_format="some")

def test_handlers_formats(handlers):
    assert len(handlers.formats) > 0
