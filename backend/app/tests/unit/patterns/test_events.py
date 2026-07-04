from app.events.event_dispatcher import EventDispatcher, Event


def test_event_dispatcher_register():
    dispatcher = EventDispatcher()
    called = []

    def handler(event: Event):
        called.append(event.name)

    dispatcher.register("test.event", handler)
    dispatcher.dispatch(Event(name="test.event"))
    assert len(called) == 1


def test_event_dispatcher_no_handler():
    dispatcher = EventDispatcher()
    dispatcher.dispatch(Event(name="unknown.event"))


def test_event_dispatcher_clear():
    dispatcher = EventDispatcher()
    dispatcher.register("test", lambda e: None)
    dispatcher.clear()
    assert len(dispatcher._handlers) == 0
