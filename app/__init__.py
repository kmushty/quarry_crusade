"""
Quarry Crusade Application
Initializes paths and exposes main components.
"""

import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add generated DDS code to Python path
generated_path = str(Path(__file__).parent.parent / "generated")
if generated_path not in sys.path:
    sys.path.append(generated_path)
    logger.info(f"Added generated DDS code path: {generated_path}")

# Import DDS components
from .dds.base.handler import DdsHandler
# from .dds.base.publisher import DdsPublisher
from .dds.base.subscriber import DdsSubscriber

# Import specific DDS implementations
from .dds.subscribers.hxgn_event import HxgnEventSubscriber

__all__ = [
    'DdsHandler',
    'DdsPublisher',
    'DdsSubscriber',
    'HxgnEventSubscriber'    
]
