"""Views for the pyramid learning journal application."""
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound
)
from pyramid.security import remember, forget
from learning_journal.security import check_credentials
from learning_journal.models.entries import Entry
import os
import datetime



@view_config(
    route_name='list_view',
    renderer='../templates/index.jinja2'
)
def list_view(request):
    """List of journal entries."""
    entries = request.dbsession.query(Entry).all()
    return {'entries': entries}


@view_config(
    route_name='detail_view',
    renderer='../templates/detail.jinja2'
)
def detail_view(request):
    """View details of an entry."""
    entry_id = int(request.matchdict['id'])
    #entry = list(filter(lambda item: item['id'] == entry_id, ENTRIES))
    # except IndexError:
    entries = request.dbsession.query(Entry).get(entry_id)
    if not entries:
        raise HTTPNotFound

    return {
        #'title': 'Detail',
        'entries': entries
    }


@view_config(
    route_name='create_view',
    renderer='../templates/new_entry.jinja2',
    permission='secret'
)
def create_view(request):
    """Create new journal entry instance."""
    if request.method == "POST" and request.POST:
        if not request.POST['title'] or not request.POST['body']:
            return {
                'title': request.POST['title'],
                'body': request.POST['body'],
                'error': "Hey dude, you're missing a little something"
            }
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body'],
            creation_date=datetime.datetime.now()
        )
        request.dbsession.add(new_entry)
        return HTTPFound(
            location=request.route_url('list_view')
        )

    return {}


@view_config(
    route_name='update_view',
    renderer='../templates/edit.jinja2',
    permission='secret'
)
def update_view(request):
    """Update existing journal entries."""
    the_id = int(request.matchdict['id'])
    session = request.dbsession
    entries = session.query(Entry).get(the_id)
    if not entries:
        raise HTTPNotFound
    # with a get request, show the existing content in the form
    if request.method == "GET":
        return {
            "title": entries.title,
            "body": entries.body
        }
    # with a post request, add the updated content to the database
    if request.method == "POST":
        entries.title = request.POST['title']
        # import pdb; pdb.set_trace()
        entries.body = request.POST['body']
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail_view', id=entries.id))


@view_config(
    route_name='login',
    renderer='../templates/login.jinja2')
def login(request):
    """Login the user."""
    if request.method == 'POST':
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('list_view'), headers=headers)
        return {'error': 'Bad username or password'}
    return {}


@view_config(route_name='logout')
def logout(request):
    """Logout the user."""
    headers = forget(request)
    return HTTPFound(request.route_url('list_view'), headers=headers)
