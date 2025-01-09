"""
Base DDS Subscriber class.
"""

from typing import Any, Dict, Callable
from .handler import DdsHandler
import threading
import time


class DdsSubscriber:
    """
    Base subscriber class for DDS communication.
    """
    
    def __init__(
        self, 
        handler: DdsHandler,
        topic_name: str,
        callback: Callable[[Dict[str, Any]], None]
    ):
        """
        Initialize the subscriber.
        
        Args:
            handler: Initialized DDS handler
            topic_name: Name of the topic to subscribe to
            callback: Function to call when data is received
        """
        self.handler = handler
        self.topic_name = topic_name
        self.callback = callback
        self.reader = self.handler.connector.get_input(topic_name)
        self.running = False
        self._read_thread = None

    def start(self) -> None:
        """
        Start listening for data.
        """
        if not self.running:
            self.running = True
            self._read_thread = threading.Thread(target=self._read_loop)
            self._read_thread.daemon = True
            self._read_thread.start()

    def stop(self) -> None:
        """
        Stop listening for data.
        """
        self.running = False
        if self._read_thread:
            self._read_thread.join(timeout=1.0)

    def _read_loop(self) -> None:
        """
        Main loop for reading data.
        """
        while self.running:
            try:
                self.reader.wait(timeout=1000)
                self.reader.take()
                for sample in self.reader.samples.valid_data_iter:
                    data = sample.get_dictionary()
                    self.callback(data)
            except Exception as e:
                print(f"Error reading from {self.topic_name}: {str(e)}")
            time.sleep(0.1)