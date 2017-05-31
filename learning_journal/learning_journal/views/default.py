"""Views for the pyramid learning journal application."""
from pyramid.view import view_config
from .data.entries import ENTRIES
from pyramid.httpexceptions import HTTPNotFound
import os


HERE = os.path.dirname(__file__)


@view_config(
    route_name='list_view',
    renderer='../templates/index.jinja2'
)
def list_view(request):
    """List of journal entries."""
    return {
        'title': 'Main',
        'entries': ENTRIES
    }


@view_config(
    route_name='detail_view',
    renderer='../templates/detail.jinja2'
)
def detail_view(request):
    """View details of an entry."""
    entry_id = int(request.matchdict['id'])
    try:
        entry = ENTRIES[entry_id]
    except IndexError:
        raise HTTPNotFound
    return {
        'title': 'Detail',
        'entries': entry
    }


@view_config(
    route_name='create_view',
    renderer='../templates/new_entry.jinja2'
)
def create_view(request):
    """Create new journal entries."""
    return {}


@view_config(
    route_name='update_view',
    renderer='../templates/edit.jinja2'
)
def update_view(request):
    """Update existing journal entries."""
    return {}
