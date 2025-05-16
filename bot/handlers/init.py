from .admin import setup as admin_handlers
from .download import setup as download_handlers
from .search import setup as search_handlers
from .user import setup as user_handlers

def register_handlers(application):
    user_handlers(application)
    search_handlers(application)
    download_handlers(application)
    admin_handlers(application)