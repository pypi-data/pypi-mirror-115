class EventHandler:
    def handle_event(self, context, event) -> None:
        raise NotImplementedError

    def shutdown(self) -> None:
        # Do nothing by default
        pass
