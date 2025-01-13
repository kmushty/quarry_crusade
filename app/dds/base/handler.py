"""
Base DDS Handler for initializing and managing DDS connections.
"""

import rti.connextdds as dds
from typing import Optional

class DdsHandler:
    """
    Base class for DDS communication handling.
    Manages the lifecycle of the DDS domain participant.
    """
    
    def __init__(self, domain_id: int):
        """
        Initialize DDS Handler.
        
        Args:
            domain_id: The domain ID for the DDS participant.
        """
        self.domain_id = domain_id
        self.participant: Optional[dds.DomainParticipant] = None

    def init_participant(self) -> None:
        """
        Initialize the DDS domain participant if not already initialized.
        """
        if not self.participant:
            try:
                print(f"Initializing DDS participant for domain {self.domain_id}")
                self.participant = dds.DomainParticipant(self.domain_id)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize DDS participant: {str(e)}")

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