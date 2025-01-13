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
        subscriber_name: str,
        callback: Callable[[Dict[str, Any]], None]
    ):
        """
        Initialize the subscriber.
        
        Args:
            handler: Initialized DDS handler
            subscriber_name: Name of the subscriber
            callback: Function to call when data is received
        """
        if not handler.connector:
            raise RuntimeError("DDS Handler not initialized")
            
        self.handler = handler
        self.input = handler.connector.get_input(subscriber_name)
        self.callback = callback
        self.running = False
        self._read_thread = None

    def _process_data(self, _):
        """
        Process received data and call the callback.
        """
        self.input.take()
        for sample in self.input.samples.valid_data_iter:
            data = sample.get_dictionary()
            self.callback(data)

    def start(self):
        """
        Start the subscriber in a separate thread.
        """
        if not self.running:
            self.running = True
            self._read_thread = threading.Thread(target=self._read_loop)
            self._read_thread.daemon = True
            self._read_thread.start()

    def stop(self):
        """
        Stop the subscriber.
        """
        self.running = False
        if self._read_thread:
            self._read_thread.join(timeout=1.0)

    def _read_loop(self):
        """
        Main loop for reading data.
        """
        while self.running:
            try:
                # Wait for data with timeout
                if self.input.wait(timeout=1000):  # 1 second timeout
                    self._process_data()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in read loop: {str(e)}")
                time.sleep(1)  # Prevent tight loop on error