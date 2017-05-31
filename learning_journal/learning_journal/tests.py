from pyramid import testing
from pyramid.response import Response
import pytest
import os
import io

HERE = os.path.dirname(__file__)


@pytest.fixture
def httprequest():
    req = testing.DummyRequest()
    return req


def test_html_views_return_response(httprequest):
    """Home view returns a reponse object."""
    from learning_journal.views.default import (
        list_view,
        detail_view,
        create_view,
        update_view
    )
    assert isinstance(list_view(httprequest), Response)
    assert isinstance(detail_view(httprequest), Response)
    assert isinstance(create_view(httprequest), Response)
    assert isinstance(update_view(httprequest), Response)


def test_list_view_return_proper_content(httprequest):
    """Home view has file content."""
    from learning_journal.views.default import list_view
    file_content = io.open(os.path.join(HERE, 'scripts/index.html')).read()
    response = list_view(httprequest)
    assert file_content == response.text


def test_list_view_is_good():
    """Home view response has file content."""
    from learning_journal.views.default import list_view
    response = list_view(httprequest)
    assert response.status_code == 200


# def test_home_view_raise_exception():
#     """Home view raise exception."""
#     from pyramid_learning_journal.views.default import list_view
#     response =
