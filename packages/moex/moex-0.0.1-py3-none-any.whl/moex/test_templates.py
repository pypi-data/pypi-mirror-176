# -*- coding: utf-8 -*-
from types import MappingProxyType

import pytest

from moex.data_classes import Template
from moex.exceptions import TemplateSearchError, TemplateRenderError
from moex.templates import TemplatesRepository
from moex.tests_fixtures import client_session


@pytest.fixture
def templates_repository():
    return TemplatesRepository()

@pytest.fixture
def bad_id(): return 2022

@pytest.fixture
def good_id(): return 13

async def test_load_data(client_session, templates_repository):
    await templates_repository.load_data(client_session)
    assert isinstance(templates_repository._data, MappingProxyType)
    assert len(templates_repository.ids) > 0

async def test_show_template_doc(templates_repository, client_session, good_id):
    errors = await templates_repository.show_template_doc(client_session, good_id)
    assert errors is None

async def test_show_template_doc_bad_id(templates_repository, client_session, bad_id):
    errors = await templates_repository.show_template_doc(client_session, bad_id)
    assert errors is None

def test_get_template(templates_repository):
    template = templates_repository.get_template(5)
    assert isinstance(template, Template)

def test_get_template_bad_id(templates_repository, bad_id):
    with pytest.raises(TemplateSearchError):
        templates_repository.get_template(bad_id)

def test_render_template(templates_repository, good_id):
    url = templates_repository.render_template(good_id, security="some_value")
    assert url == "http://iss.moex.com/iss/securities/some_value"

def test_render_template_bad_id(templates_repository, bad_id):
    with pytest.raises(TemplateSearchError):
        templates_repository.render_template(bad_id, security="some_value")

def test_render_template_without_vars(templates_repository, good_id):
    with pytest.raises(TemplateRenderError):
        templates_repository.render_template(good_id)

def test_find_template_not_exist(templates_repository):
    with pytest.raises(StopIteration):
        next(templates_repository.find_template_id("/SOME-VALUE"))

def test_find_template_id(templates_repository):
    template = templates_repository.find_template_id("/history/")
    assert next(template) is not None
