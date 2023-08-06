import click
from levo_commons import events

from ....handlers import EventHandler
from ..context import ExecutionContext


class DefaultOutputStyleHandler(EventHandler):
    def handle_event(self, context: ExecutionContext, event: events.Event) -> None:
        """Choose and execute a proper handler for the given event."""
        if isinstance(event, events.Initialized):
            click.echo("Start test session")
        if isinstance(event, events.BeforeTestCaseExecution):
            click.echo("Before test case")
        if isinstance(event, events.AfterTestCaseExecution):
            click.echo("After test case")
        if isinstance(event, events.BeforeTestStepExecution):
            click.echo("Before test step")
        if isinstance(event, events.AfterTestStepExecution):
            click.echo("After test step")
        if isinstance(event, events.Finished):
            click.echo("Test session finished!")
        if isinstance(event, events.Interrupted):
            click.echo("Interrupted!")
        if isinstance(event, events.InternalError):
            click.echo("Internal error")
