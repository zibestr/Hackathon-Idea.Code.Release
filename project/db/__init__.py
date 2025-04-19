from .connections import (
    create_models,
    init_db,
    get_session
)

try:
    from .models import *
except ImportError:
    import asyncio
    asyncio.run(create_models('db/models.py'))
    from .models import *

from queries import *

__all__ = [
    'create_models',
    'init_db',
    'get_session'
]
