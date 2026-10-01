from app.shared.events import AnomalyDetected, EventBus, RunIngested


def test_publish_delivers_event_to_subscribed_handler():
    # Arrange
    bus, received = EventBus(), []
    bus.subscribe(RunIngested, received.append)
    event = RunIngested(run_id="r1", pipeline="orders_daily")
    # Act
    delivered = bus.publish(event)
    # Assert
    assert delivered == 1
    assert received == [event]


def test_publish_does_not_deliver_other_event_types():
    bus, received = EventBus(), []
    bus.subscribe(AnomalyDetected, received.append)

    delivered = bus.publish(RunIngested(run_id="r1", pipeline="p"))

    assert delivered == 0
    assert received == []


def test_failing_handler_does_not_block_other_handlers():
    bus, received = EventBus(), []

    def broken(_event):
        raise RuntimeError("boom")

    bus.subscribe(RunIngested, broken)
    bus.subscribe(RunIngested, received.append)

    delivered = bus.publish(RunIngested(run_id="r2", pipeline="p"))

    assert delivered == 1
    assert len(received) == 1
