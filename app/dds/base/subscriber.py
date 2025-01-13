"""
Base DDS Subscriber class.
"""
import rti.connextdds as dds
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
        xml_path: str,
        type_name: str,
        callback: Callable[[Dict[str, Any]], None]
    ):
        """
        Initialize the subscriber.
        
        Args:
            handler: Initialized DDS handler
            topic_name: Name of the topic to subscribe to
            xml_path: Path to the XML file containing the QoS configuration
            type_name: Name of the data type
            callback: Function to call when data is received
        """
        try:
            self.qos_provider = dds.QosProvider(f"file://{xml_path}")
            print(f"QoS provider initialized from {xml_path}")
            # Get the dynamic type from XML
            self.dynamic_type = self.qos_provider.type(type_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load XML configuration or type: {str(e)}")
        
        # Create topic using dynamic type
        self.topic = dds.Topic(
            self.handler.participant,
            topic_name,
            self.dynamic_type,
            self.qos_provider.topic_qos
        )
        
        # Create reader using dynamic type
        self.reader = dds.DataReader(
            self.handler.participant.implicit_subscriber,
            self.topic,
            self.qos_provider.datareader_qos
        )
        self.callback = callback
        self.running = False
        self._read_thread = None

        # Set up the status condition and waitset
        self.status_condition = dds.StatusCondition(self.reader)
        self.status_condition.enabled_statuses = dds.StatusMask.DATA_AVAILABLE
        self.status_condition.set_handler(self._on_data_available)

        self.waitset = dds.WaitSet()
        self.waitset += self.status_condition

    def _on_data_available(self, _):
        """
        Handler for data available status.
        """
        self.reader.take()
        for sample in self.reader.samples.valid_data_iter:
            self.callback(sample.data)

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
                self.waitset.dispatch(dds.Duration(1))
            except KeyboardInterrupt:
                break