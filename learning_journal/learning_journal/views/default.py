"""Views for the pyramid learning journal application."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.models.entries import Entry
import os


HERE = os.path.dirname(__file__)


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
    # print(entry_id)
    # try:
        # entry = None
        # for item in ENTRIES:
        #     if item['id'] == entry_id
        #     entry = item
        #     break
    entry = list(filter(lambda item: item['id'] == entry_id, ENTRIES))    
    # except IndexError:
    if not entry:
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


# @view_config(
#     route_name='update_view',
#     renderer='../templates/edit.jinja2'
# )
# def update_view(request):
#     """Update existing journal entries."""
#     return {}
