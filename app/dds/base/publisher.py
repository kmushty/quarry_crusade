"""
Base DDS Publisher class.
"""
from typing import Any, Dict
from .handler import DdsHandler
import rticonnextdds_connector as rti

class DdsPublisher:
    """
    Base publisher class for DDS communication.
    """
    
    def __init__(
        self, 
        handler: DdsHandler,
        publisher_name: str
    ):
        """
        Initialize the publisher.
        
        Args:
            handler: Initialized DDS handler
            publisher_name: Name of the publisher configuration in XML
        """
        if not handler.connector:
            raise RuntimeError("DDS Handler not initialized")
            
        self.handler = handler
        self.output = handler.connector.get_output(publisher_name)

    def write(self, data: Dict[str, Any]) -> None:
        """
        Write data to DDS.
        
        Args:
            data: Dictionary containing the data to write
        """
        try:
            # Set the instance data
            for key, value in data.items():
                self.output.instance.set_dictionary(data)
            
            # Write the instance
            self.output.write()
        except Exception as e:
            print(f"Error writing data: {str(e)}")

    def dispose(self) -> None:
        """
        Dispose of the publisher.
        """
        try:
            self.output.dispose()
        except Exception as e:
            print(f"Error disposing publisher: {str(e)}")