"""
DDS (Data Distribution Service) package for Quarry Crusade.
This package handles DDS communications for Event messages.
"""

# Import base classes
from .base.handler import DdsHandler

# Import subscribers
from .subscribers.hxgn_event import HxgnEventSubscriber

# Version of the DDS package
__version__ = '1.0.0'

__all__ = [
    # Base classes
    'DdsHandler',
    
    # Subscribers
    'HxgnEventSubscriber',
]

DEFAULT_DOMAIN_ID = 7  # MATTERHORN_MMS_DOMAIN_ID

def get_domain_id():
    """Returns the default DDS domain ID for the application."""
    return DEFAULT_DOMAIN_ID
