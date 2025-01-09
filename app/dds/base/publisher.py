"""
Base DDS Publisher class.
"""

from typing import Any, Dict
from .handler import DdsHandler


class DdsPublisher:
    """
    Base publisher class for DDS communication.
    """
    
    def __init__(
        self, 
        handler: DdsHandler,
        topic_name: str
    ):
        """
        Initialize the publisher.
        
        Args:
            handler: Initialized DDS handler
            topic_name: Name of the topic to publish to
        """
        self.handler = handler
        self.topic_name = topic_name
        self.writer = self.handler.connector.get_output(topic_name)

    def publish(self, data: Dict[str, Any]) -> None:
        """
        Publish data to the topic.
        
        Args:
            data: Dictionary containing the data to publish
        """
        try:
            self.writer.instance.set_dictionary(data)
            self.writer.write()
        except Exception as e:
            raise RuntimeError(f"Failed to publish to {self.topic_name}: {str(e)}")