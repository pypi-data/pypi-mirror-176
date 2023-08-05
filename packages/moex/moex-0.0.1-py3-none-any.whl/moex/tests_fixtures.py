# -*- coding: utf-8 -*-
import pytest
from aiohttp import ClientSession

# pytestmark = pytest.mark.asyncio

@pytest.fixture
async def client_session():
    async with ClientSession() as session:
        yield session
