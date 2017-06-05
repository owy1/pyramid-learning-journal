from pyramid import testing
from pyramid.response import Response
from learning_journal.models.meta import Base
from learning_journal.models import (
    Entry,
    get_tm_session,
)
from pyramid.config import Configurator
import transaction
import pytest
import os
import io

HERE = os.path.dirname(__file__)
SITE_ROOT = 'http://localhost'


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


# def test_detail_view_contains_attr():
#     """Test that what's returned by view contains journal object."""
#     from learning_journal.views.default import detail_view
#     request = testing.DummyRequest()
#     info = detail_view(request)
#     for key in ["category", "creation_date", "id", "description", "amount"]:
#         assert key in info.keys()


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.
    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.
    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://kurtrm:hofbrau@localhost:5432/learning_journal'
    })
    config.include("learning_journal.models")
    config.include("learning_journal.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database.
    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    from pyramid import testing
    req = testing.DummyRequest()
    req.dbsession = db_session
    return req


@pytest.fixture
def post_request(dummy_request):
    dummy_request.method = "POST"
    return dummy_request


def test_create_view_post_empty_data_returns_empty_dict(post_request):
    from learning_journal.views.default import create_view
    response = create_view(post_request)
    assert response == {}


def test_create_view_post_incomplete_data_returns_error(post_request):
    from learning_journal.views.default import create_view
    data = {
        'title': '',
        'body': ''
    }
    post_request.POST = data
    response = create_view(post_request)
    assert 'error' in response


def test_create_view_post_incomplete_data_returns_data(post_request):
    from learning_journal.views.default import create_view
    data = {
        'title': '170815_ophelia',
        'body': ''
    }
    post_request.POST = data
    response = create_view(post_request)
    assert 'title' in response
    assert 'body' in response
    assert response['title'] == '170815_ophelia'
    assert response['body'] == ''


def test_create_view_post_with_data_redirects(post_request):
    from learning_journal.views.default import create_view
    from pyramid.httpexceptions import HTTPFound
    data = {
        'title': '170815_ophelia',
        'body': 'Day zero testing.'
    }
    post_request.POST = data
    response = create_view(post_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


@pytest.fixture(scope="session")
def testapp(request):
    """Create an instance of our app for testing."""
    from webtest import TestApp

    def main(global_config, **settings):
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.models')
        config.include('learning_journal.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({}, **{"sqlalchemy.url": "postgres:///test_entries"})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factor"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)
    return testapp


def test_new_entry_redirects_to_home(testapp):
    """When redirection is followed, result is home page."""
    data = {
        'title': '170815_ophelia',
        'body': 'Day zero testing.'
    }
    response = testapp.post('/entries/new_entry', data)
    assert response.location == SITE_ROOT + "/"


def test_new_entry_redirects_to_home_and_shows_html(testapp):
    """When redirection is followed, result is home page."""
    data = {
        'title': '170815_ophelia',
        'body': 'Day zero testing.'
    }
    response = testapp.post('/entry/new_entry', data).follow()
    assert "<h1>List of Entries</h1>" in response.text

    assert len(ENTRIES) == len(html.findAll("article"))
