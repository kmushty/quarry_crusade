"""
Base DDS Handler for initializing and managing DDS connections.
"""

import rticonnextdds_connector as dds
from typing import Optional

class DdsHandler:
    """
    Base class for DDS communication handling.
    Manages the lifecycle of the DDS domain participant.
    """
    
    def __init__(self, xml_path: str, participant_name: str):
        """
        Initialize DDS Handler.
        
        Args:
            xml_path: The path to the XML file containing the QoS configuration
            participant_name: The name of the participant
        """
        self.xml_path = xml_path
        self.participant_name = participant_name
        self.participant: Optional[dds.DomainParticipant] = None

    def init_participant(self) -> None:
        """
        Initialize the DDS connector if not already initialized.
        """
        try:
            print("In Handler: Initializing DDS connector")
            print(f"Initializing DDS connector with config {self.participant_name}")
            self.connector = dds.Connector(
                config_name=self.participant_name,
                url=f"file://{self.xml_path}"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize DDS connector: {str(e)}")


    def cleanup(self) -> None:
        """
        Clean up DDS.
        """
        if self.participant:
            try:
                self.participant.close()
                self.participant = None
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")

    def __enter__(self):
        """
        Context manager entry.
        """
        self.init_participant()
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