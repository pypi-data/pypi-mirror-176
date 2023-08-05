# -*- coding: utf-8 -*-
import pytest

from moex.api import AIOMoex
from moex.exceptions import HandlersSearchError
from moex.tests_fixtures import client_session


@pytest.fixture
def output_format(): return ".json"

@pytest.fixture
def output_format_bad(): return "smth"

@pytest.fixture
async def aiomoex(client_session, output_format):
    aiomoex = AIOMoex()
    await aiomoex.load(session=client_session, output_format=output_format)
    return aiomoex

async def test_load(aiomoex):
    assert len(aiomoex.templates) > 0

async def test_load_fail(aiomoex, client_session, output_format_bad):
    with pytest.raises(HandlersSearchError):
        await aiomoex.load(session=client_session, output_format=output_format_bad)

def test_show_templates(aiomoex):
    errors = aiomoex.show_templates()
    assert errors is None
