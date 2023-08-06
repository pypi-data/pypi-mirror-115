import base64
import enum
import os
import time
import traceback
from typing import Dict, List, Optional, Union, cast

from levo_commons import events
from reportportal_client import ReportPortalService
from schemathesis.cli.handlers import get_unique_failures
from schemathesis.constants import CodeSampleStyle

from ....apitesting.runs.api_test_runs_pb2 import (  # type: ignore
    CATEGORY_FAILED,
    CATEGORY_SUCCESS,
    ApiEndpointTestsCategory,
)
from ....env_constants import BASE_URL
from ....handlers import EventHandler
from ....utils import fetch_schema_as_lines
from ..context import ExecutionContext
from ..models import (
    AfterExecutionPayload,
    BeforeExecutionPayload,
    FinishedPayload,
    Response,
    SerializedCase,
    SerializedError,
    SerializedTestResult,
    Status,
)

DISABLE_SCHEMA_VALIDATION_MESSAGE = (
    "\nYou can disable input schema validation with --validate-schema=false "
    "command-line option\nIn this case, Schemathesis cannot guarantee proper"
    " behavior during the test run"
)

TEST_RUNS_SERVICE_URL = os.getenv("TEST_RUNS_SERVICE_URL", BASE_URL + "/test-runs")


def timestamp():
    return str(int(time.time() * 1000))


def handle_before_execution(
    context: ExecutionContext,
    event: events.BeforeTestCaseExecution[BeforeExecutionPayload],
    service: ReportPortalService,
) -> None:
    message = event.payload.verbose_name
    if event.payload.recursion_level > 0:
        message = f"{'    ' * event.payload.recursion_level}-> {message}"
        # This value is not `None` - the value is set in runtime before this line
        context.operations_count += 1  # type: ignore
    item_id = service.start_test_item(
        name=message,
        description=f"{event.payload.method} {event.payload.relative_path}",
        start_time=timestamp(),
        item_type="TEST",
    )
    context.correlation_id_to_item_id[event.payload.correlation_id] = item_id


def handle_after_execution(
    context: ExecutionContext,
    event: events.AfterTestCaseExecution[AfterExecutionPayload],
    service: ReportPortalService,
) -> None:
    context.hypothesis_output.extend(event.payload.hypothesis_output)
    context.operations_processed += 1
    context.results.append(event.payload.result)
    status_dict = {
        Status.success: "PASSED",
        Status.failure: "FAILED",
        Status.error: "FAILED",
    }
    status = status_dict[event.payload.status]

    check_summary: Dict[str, ApiEndpointTestsCategory] = {}

    for check in event.payload.result.checks:
        check_item_id = service.start_test_item(
            name=check.name,
            description=f"{check.message}",
            start_time=timestamp(),
            item_type="STEP",
            parent_item_id=context.correlation_id_to_item_id[
                event.payload.correlation_id
            ],
        )
        if check.name not in check_summary:
            check_summary[check.name] = ApiEndpointTestsCategory(
                name=check.name,
                successful_tests=0,
                failed_tests=0,
                duration_millis=0,
                status=CATEGORY_SUCCESS,
            )
        check_summary[check.name].duration_millis += check.duration
        if check.value == Status.success:
            check_summary[check.name].successful_tests += 1
        else:
            check_summary[check.name].failed_tests += 1
        if (
            check.value != Status.success
            and check_summary[check.name].status != CATEGORY_FAILED
        ):
            check_summary[check.name].status = CATEGORY_FAILED
        service.finish_test_item(
            item_id=check_item_id,
            end_time=timestamp(),
            status=status_dict[check.value],
        )

    test_item_attributes = {
        "elapsed_time": event.payload.elapsed_time,
        "correlation-id": event.payload.correlation_id,
        "thread-id": event.payload.thread_id,
        "seed": event.payload.result.seed,
        "data_generation_method": event.payload.result.data_generation_method,
    }

    for check_name in check_summary:
        test_item_attributes[f"check:{check_name}"] = base64.b64encode(
            check_summary[check_name].SerializeToString()
        ).decode("utf-8")

    service.finish_test_item(
        item_id=context.correlation_id_to_item_id[event.payload.correlation_id],
        end_time=timestamp(),
        status=status,
        # issue=str(event.result.errors) if event.result.has_errors else None,
        attributes=test_item_attributes,
    )
    if event.payload.hypothesis_output is not None:
        report_log(
            message=str(event.payload.hypothesis_output),
            service=service,
            item_id=context.correlation_id_to_item_id[event.payload.correlation_id],
        )
    if event.payload.result.has_errors:
        report_log(
            message=get_single_error(context, event.payload.result),
            service=service,
            level="ERROR",
            item_id=context.correlation_id_to_item_id[event.payload.correlation_id],
        )
    if event.payload.result.has_failures:
        report_log(
            message=get_failures_for_single_test(context, event.payload.result),
            service=service,
            level="ERROR",
            item_id=context.correlation_id_to_item_id[event.payload.correlation_id],
        )


def get_hypothesis_output(hypothesis_output: List[str]) -> Optional[str]:
    """Show falsifying examples from Hypothesis output if there are any."""
    if hypothesis_output:
        return get_section_name("HYPOTHESIS OUTPUT") + "\n".join(hypothesis_output)
    return None


def get_errors(
    context: ExecutionContext, event: events.Finished[FinishedPayload]
) -> Optional[str]:
    """Get all errors in the test run."""
    if not event.payload.has_errors:
        return None

    lines = [get_section_name("ERRORS")]
    for result in context.results:
        if not result.has_errors:
            continue
        lines.append(get_single_error(context, result))
    if event.payload.generic_errors:
        lines.append(get_generic_errors(context, event.payload.generic_errors))
    return "\n".join(lines)


def get_single_error(
    context: ExecutionContext,
    result: SerializedTestResult,
) -> str:
    lines = [get_subsection(result)]
    for error in result.errors:
        lines.append(_get_error(context, error, result.seed))
    return "\n".join(lines)


def get_generic_errors(
    context: ExecutionContext,
    errors: List[SerializedError],
) -> str:
    lines = []
    for error in errors:
        lines.append(get_section_name(error.title or "Generic error", "_"))
        lines.append(_get_error(context, error))
    return "\n".join(lines)


def _get_error(
    context: ExecutionContext,
    error: SerializedError,
    seed: Optional[int] = None,
) -> str:
    if context.show_errors_tracebacks:
        message = error.exception_with_traceback
    else:
        message = error.exception
    if error.exception.startswith("InvalidSchema") and context.validate_schema:
        message += DISABLE_SCHEMA_VALIDATION_MESSAGE + "\n"
    if error.example is not None:
        get_example(context, error.example, seed=seed)
    return message


def get_failures(
    context: ExecutionContext, event: events.Finished[FinishedPayload]
) -> Optional[str]:
    """Get all failures in the test run."""
    if not event.payload.has_failures:
        return None
    relevant_results = [result for result in context.results if not result.is_errored]
    if not relevant_results:
        return None
    lines = [get_section_name("FAILURES")]
    for result in relevant_results:
        if not result.has_failures:
            continue
        lines.append(get_failures_for_single_test(context, result))
    return "\n".join(lines)


def get_failures_for_single_test(
    context: ExecutionContext,
    result: SerializedTestResult,
) -> str:
    """Gets a failure for a single method / path."""
    lines = [get_subsection(result)]
    checks = get_unique_failures(result.checks)
    for idx, check in enumerate(checks, 1):
        message: Optional[str]
        if check.message:
            message = f"{idx}. {check.message}"
        else:
            message = None
        lines.append(
            get_example(context, check.example, check.response, message, result.seed)
        )
    return "\n".join(lines)


def reduce_schema_error(message: str) -> str:
    """Reduce the error schema output."""
    end_of_message_index = message.find(":", message.find("Failed validating"))
    if end_of_message_index != -1:
        return message[:end_of_message_index]
    return message


def get_example(
    context: ExecutionContext,
    case: SerializedCase,
    response: Optional[Response] = None,
    message: Optional[str] = None,
    seed: Optional[int] = None,
) -> str:
    lines = []
    if message is not None:
        if not context.verbosity:
            lines.append(reduce_schema_error(message))
    for line in case.text_lines:
        lines.append(line)

    if response is not None and response.body is not None:
        payload = base64.b64decode(response.body).decode(
            response.encoding or "utf8", errors="replace"
        )
        lines.append(f"----------\n\nResponse payload: `{payload}`\n")
    if context.code_sample_style == CodeSampleStyle.python:
        lines.append(
            f"Run this Python code to reproduce this failure: \n\n    {case.requests_code}\n"
        )
    if context.code_sample_style == CodeSampleStyle.curl:
        lines.append(
            f"Run this cURL command to reproduce this failure: \n\n    {case.curl_code}\n"
        )
    if seed is not None:
        lines.append(
            f"Or add this option to your command line parameters: --hypothesis-seed={seed}"
        )
    return "\n".join(lines)


def get_subsection(
    result: SerializedTestResult,
) -> str:
    return get_section_name(result.verbose_name, "_", result.data_generation_method)


def get_statistic(event: events.Finished[FinishedPayload]) -> str:
    """Format and print statistic collected by :obj:`models.TestResult`."""
    lines = [get_section_name("SUMMARY")]
    total = event.payload.total
    if event.payload.is_empty or not total:
        lines.append("No checks were performed.")

    if total:
        lines.append(get_checks_statistics(total))

    return "\n".join(lines)


def get_checks_statistics(total: Dict[str, Dict[Union[str, Status], int]]) -> str:
    lines = []
    for check_name, results in total.items():
        lines.append(get_check_result(check_name, results))
    return "Performed checks:" + "\n".join(lines)


def get_check_result(
    check_name: str,
    results: Dict[Union[str, Status], int],
) -> str:
    """Show results of single check execution."""
    success = results.get(Status.success, 0)
    total = results.get("total", 0)
    return check_name + ": " + f"{success} / {total} passed"


def get_internal_error(
    context: ExecutionContext, event: events.InternalError
) -> Optional[str]:
    message = None
    if event.exception:
        if context.show_errors_tracebacks:
            message = event.exception_with_traceback
        else:
            message = event.exception
        message = (
            f"Error: {message}\n"
            f"Add this option to your command line parameters to see full tracebacks: --show-errors-tracebacks"
        )
        if event.exception_type == "jsonschema.exceptions.ValidationError":
            message += "\n" + DISABLE_SCHEMA_VALIDATION_MESSAGE
    return message


def get_summary(event: events.Finished[FinishedPayload]) -> str:
    message = get_summary_output(event)
    return get_section_name(message)


def get_summary_message_parts(event: events.Finished[FinishedPayload]) -> List[str]:
    parts = []
    passed = event.payload.passed_count
    if passed:
        parts.append(f"{passed} passed")
    failed = event.payload.failed_count
    if failed:
        parts.append(f"{failed} failed")
    errored = event.payload.errored_count
    if errored:
        parts.append(f"{errored} errored")
    return parts


def get_summary_output(event: events.Finished[FinishedPayload]) -> str:
    parts = get_summary_message_parts(event)
    if not parts:
        message = "Empty test suite"
    else:
        message = f'{", ".join(parts)} in {event.running_time:.2f}s'
    return message


def get_section_name(title: str, separator: str = "=", extra: str = "") -> str:
    """Print section name with separators in terminal with the given title nicely centered."""
    extra = extra if not extra else f" [{extra}]"
    return f" {title}{extra} ".center(80, separator)


def handle_finished(
    event: events.Finished[FinishedPayload], service: ReportPortalService
) -> None:
    """Show the outcome of the whole testing session."""
    report_log(get_statistic(event), service)
    report_log(get_summary(event), service)


def report_log(
    message: str, service: ReportPortalService, level="INFO", item_id=None
) -> None:
    if message is None:
        return
    service.log(time=timestamp(), message=message, item_id=item_id, level=level)


def my_error_handler(exc_info):
    """
    This callback function will be called by async service client when error occurs.
    Return True if error is not critical and you want to continue work.
    :param exc_info: result of sys.exc_info() -> (type, value, traceback)
    :return:
    """
    traceback.print_exception(*exc_info)


def terminate_launch(service: ReportPortalService, status="PASSED") -> None:
    service.finish_launch(end_time=timestamp(), status=status)
    service.terminate()


class HandlerState(enum.Enum):
    """Different states for ReportPortal handler lifecycle."""

    # Instance is created. The default state
    NEW = enum.auto()
    # Launch started, ready to handle events
    ACTIVE = enum.auto()
    # Launch is interrupted, no events will be processed after it
    INTERRUPTED = enum.auto()


class ReportPortalHandler(EventHandler):
    def __init__(self, project, token, spec_path):
        self.service = ReportPortalService(
            endpoint=TEST_RUNS_SERVICE_URL, project=project, token=token
        )
        self.state = HandlerState.NEW
        self.spec = fetch_schema_as_lines(spec_path)

    def _set_state(self, state: HandlerState) -> None:
        self.state = state

    def _terminate_launch(self, status: str) -> None:
        if self.state == HandlerState.ACTIVE:
            terminate_launch(self.service, status)

    def handle_event(self, context: ExecutionContext, event: events.Event) -> None:
        """Reports the test results to ReportPortal service."""
        if isinstance(event, events.Initialized):
            # Create a launch in report portal
            launch_name = "Schema testing"
            self.service.start_launch(
                name=launch_name, start_time=timestamp(), description=launch_name
            )
            self._set_state(HandlerState.ACTIVE)
            context.operations_count = cast(
                int, event.payload.operations_count
            )  # INVARIANT: should not be `None`
        if isinstance(event, events.BeforeTestCaseExecution):
            handle_before_execution(context, event, self.service)
        if isinstance(event, events.AfterTestCaseExecution):
            handle_after_execution(context, event, self.service)
        if isinstance(event, events.Finished):
            attachment = {
                "name": "schema",
                "data": "".join(self.spec),
                "mime": "text/plain",
            }
            self.service.log(timestamp(), "schema", attachment=attachment)
            handle_finished(event, self.service)
            status = {
                HandlerState.ACTIVE: "PASSED",
                HandlerState.INTERRUPTED: "INTERRUPTED",
            }[self.state]
            self._terminate_launch(status)
        if isinstance(event, events.Interrupted):
            self._set_state(HandlerState.INTERRUPTED)
        if isinstance(event, events.InternalError):
            self._terminate_launch("FAILED")
