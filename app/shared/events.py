"""In-process event bus (Observer pattern) connecting bounded contexts.

Contexts publish domain events; handlers in other contexts subscribe by event type.
Handlers run after the publishing transaction commits (events are outside the consistency
boundary). A failing handler is logged and does not break other handlers.
"""

import logging
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, TypeVar
from uuid import uuid4

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class RunIngested(DomainEvent):
    run_id: str = ""
    pipeline: str = ""


@dataclass(frozen=True)
class AnomalyDetected(DomainEvent):
    run_id: str = ""
    pipeline: str = ""
    anomaly_type: str = ""
    details: dict[str, Any] = field(default_factory=dict)


E = TypeVar("E", bound=DomainEvent)
Handler = Callable[[Any], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: type[E], handler: Callable[[E], None]) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> int:
        """Deliver the event to every subscribed handler. Returns number of successful calls."""
        delivered = 0
        for handler in list(self._handlers[type(event)]):
            try:
                handler(event)
                delivered += 1
            except Exception:  # noqa: BLE001 - isolate handler failures
                logger.exception("Handler %r failed for %s", handler, type(event).__name__)
        return delivered


bus = EventBus()
