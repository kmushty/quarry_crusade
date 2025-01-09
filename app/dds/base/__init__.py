"""
Base classes for DDS communication in Quarry Crusade.

This module provides the foundational classes for DDS communication:
- DdsHandler: Base class for DDS initialization and configuration
- DdsPublisher: Base class for all publishers
- DdsSubscriber: Base class for all subscribers

Usage:
    from app.dds.base import DdsPublisher

    class MyPublisher(DdsPublisher):
        def __init__(self):
            super().__init__("MyTopic")
"""

from .handler import DdsHandler
from .publisher import DdsPublisher
from .subscriber import DdsSubscriber

# Version of the base module
__version__ = '1.0.0'

# Define public API
__all__ = [
    'DdsHandler',
    'DdsPublisher',
    'DdsSubscriber'
]

# QoS Profile constants
DEFAULT_QOS_LIBRARY = "MissionManager_QOS_Library"
DEFAULT_QOS_PROFILE = "MissionManager_QOS_Profile"

def get_qos_settings():
    """Returns the default QoS library and profile names."""
    return {
        'library': DEFAULT_QOS_LIBRARY,
        'profile': DEFAULT_QOS_PROFILE
    }
