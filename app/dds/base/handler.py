"""
Base DDS Handler for initializing and managing DDS connections.
"""

from rticonnextdds_connector import Connector
from pathlib import Path
from typing import Optional


class DdsHandler:
    """
    Base class for DDS communication handling.
    Manages the lifecycle of the DDS connector.
    """
    
    def __init__(
        self, 
        xml_path: str,
        config_name: str,
        participant_name: Optional[str] = None
    ):
        """
        Initialize DDS Handler.
        
        Args:
            xml_path: Path to QoS XML file
            config_name: QoS configuration name (e.g., "MyLibrary::MyProfile")
            participant_name: Optional name for this participant
        """
        self.xml_path = xml_path
        self.config_name = config_name
        self.participant_name = participant_name or self.__class__.__name__
        self.connector: Optional[Connector] = None

    def init_connector(self) -> None:
        """
        Initialize the DDS connector if not already initialized.
        """
        if not self.connector:
            try:
                self.connector = Connector(
                    config_name=self.config_name,
                    url=self.xml_path
                )
            except Exception as e:
                raise RuntimeError(f"Failed to initialize DDS connector: {str(e)}")

    def cleanup(self) -> None:
        """
        Clean up DDS.
        """
        if self.connector:
            try:
                self.connector.close()
                self.connector = None
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")

    def __enter__(self):
        """
        Context manager entry.
        """
        self.init_connector()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit.
        """
        self.cleanup()

    def __del__(self):
        """
        Destructor to ensure cleanup.
        """
        self.cleanup()