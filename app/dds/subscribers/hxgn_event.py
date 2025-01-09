from ..base.subscriber import DdsSubscriber
from typing import Callable, Dict, Any, TypedDict
from enum import IntEnum

class EventLevels(IntEnum):
    EVENT_UNKNOWN = 0
    EVENT_DEBUG = 1
    EVENT_INFO = 2
    EVENT_WARNING = 3
    EVENT_ERROR = 4
    EVENT_CRITICAL = 5

class Stamp(TypedDict):
    sec: int
    nsec: int

class Header(TypedDict):
    stamp: Stamp
    seq: int

class GeoPosition(TypedDict):
    latitude: float
    longitude: float
    altitude: float

class HxgnEvent(TypedDict):
    header: Header
    equipment_id: int
    assignment_id: int
    equipment_tag: str
    position: GeoPosition
    code: str
    message: str
    level: EventLevels

class HxgnEventSubscriber(DdsSubscriber):
    def __init__(self, handler, callback: Callable[[HxgnEvent], None]):
        super().__init__(
            handler=handler,
            topic_name="Events",
            callback=self._handle_event
        )
        self.user_callback = callback
        
    def _handle_event(self, data: HxgnEvent) -> None:
        """
        Process raw DDS data.
        Maps IDL types to Python types:
        - long -> int
        - string -> str
        - double -> float
        - enum -> int (with defined constants)
        """
        try:
            event: HxgnEvent = {
                'header': {
                    'stamp': {
                        'sec': int(data.get('header', {}).get('stamp', {}).get('sec', 0)),
                        'nsec': int(data.get('header', {}).get('stamp', {}).get('nsec', 0))
                    },
                    'seq': int(data.get('header', {}).get('seq', 0))
                },
                'equipment_id': int(data.get('equipmentId', 0)),
                'assignment_id': int(data.get('assignmentId', 0)),
                'equipment_tag': str(data.get('equipmentTag', '')),
                'position': {
                    'latitude': float(data.get('position', {}).get('latitude', 0.0)),
                    'longitude': float(data.get('position', {}).get('longitude', 0.0)),
                    'altitude': float(data.get('position', {}).get('altitude', 0.0))
                },
                'code': str(data.get('code', '')),
                'message': str(data.get('message', '')),
                'level': EventLevels(data.get('level', EventLevels.EVENT_UNKNOWN))
            }
            
            self.user_callback(event)
            
        except (ValueError, TypeError) as e:
            print(f"Error processing event data: {str(e)}")
            print(f"Raw data: {data}")