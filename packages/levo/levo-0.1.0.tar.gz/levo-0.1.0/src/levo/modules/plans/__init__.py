"""The test module which communicates with Levo platform, gets the tests, runs them,
and reports the results back to Levo.
"""
import importlib
import pathlib
import time
from typing import Callable, Generator, List

import click
from levo_commons.config import PlanConfig
from levo_commons.events import Finished, Initialized
from levo_commons.utils import syspath_prepend

from ... import events
from ...config import TestPlanCommandConfig
from ...config_file import try_get_auth_config
from ...handlers import EventHandler
from . import local, remote
from .context import ExecutionContext
from .handlers.default import DefaultOutputStyleHandler
from .models import Plan

TEST_PLAN_ENTRYPOINT_NAME = "test"


class PlanEventStream(events.EventStream):
    def stop(self) -> None:
        # TODO. Implement interruption
        raise NotImplementedError


def get_test_plan_entrypoint(module_path: str) -> Callable:
    """Load test plan & extract its entrypoint."""
    module = importlib.import_module(module_path)
    return getattr(module, TEST_PLAN_ENTRYPOINT_NAME)


def should_process(path: pathlib.Path) -> bool:
    return path.is_dir() and path.name != "__pycache__"


def into_event_stream(plan: Plan, config: PlanConfig) -> events.EventStream:
    """Create a stream of Schemathesis events."""
    return PlanEventStream(iter_cases(plan, config), lambda x: x)


def iter_cases(plan: Plan, config: PlanConfig) -> Generator:
    initialized = Initialized()
    yield initialized
    for suite in plan.iter_suite():
        if not should_process(suite):
            continue
        for case in suite.iterdir():
            if not should_process(case):
                continue
            module_path = f"{plan.name}.{suite.name}.{case.name}.testcase_code"
            entrypoint = get_test_plan_entrypoint(module_path)
            yield from entrypoint(config)
    yield Finished(running_time=time.monotonic() - initialized.start_time)


def cli_entrypoint(input_config: TestPlanCommandConfig):
    auth_config = try_get_auth_config()
    handlers: List[EventHandler] = [DefaultOutputStyleHandler()]
    if input_config.test_plans_catalog:
        plan = local.get_plan(
            plan_lrn=input_config.plan_lrn, catalog=input_config.test_plans_catalog
        )
        if plan is None:
            raise click.UsageError(
                f"Can not find a plan with LRN {input_config.plan_lrn}"
            )
    else:
        plan = remote.get_plan(
            plan_lrn=input_config.plan_lrn,
            authz_header=auth_config["token_type"] + " " + auth_config["access_token"],
        )

    config = PlanConfig(
        spec_path="",  # This should be optional ideally.
        target_url=input_config.target_url,
        auth=input_config.auth,
        auth_type=input_config.auth_type,
        report_to_saas=input_config.report_to_saas,
    )
    context = ExecutionContext()

    with syspath_prepend(plan.catalog):
        event_stream = into_event_stream(plan, config)
        return events.handle(handlers, event_stream, context)
