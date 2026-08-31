"""
Event Dispatcher Pattern.
"""

from typing import Callable, List, Dict, Any


class EventDispatcher:
    _listeners: Dict[str, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_name: str, listener: Callable):
        if event_name not in cls._listeners:
            cls._listeners[event_name] = []
        cls._listeners[event_name].append(listener)

    @classmethod
    def dispatch(cls, event_name: str, payload: Dict[str, Any]):
        listeners = cls._listeners.get(event_name, [])
        for listener in listeners:
            try:
                listener(payload)
            except Exception as e:
                print(f"Error handling event {event_name}: {e}")
