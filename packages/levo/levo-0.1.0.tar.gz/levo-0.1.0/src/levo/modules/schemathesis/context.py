import os
import shutil
from typing import Dict, List, Optional

import attr
from schemathesis.constants import CodeSampleStyle

from .models import SerializedTestResult


@attr.s(slots=True)
class ExecutionContext:
    """Storage for the current context of the execution."""

    hypothesis_output: List[str] = attr.ib(factory=list)
    workers_num: int = attr.ib(default=1)
    show_errors_tracebacks: bool = attr.ib(default=False)
    validate_schema: bool = attr.ib(default=True)
    operations_processed: int = attr.ib(default=0)
    # It is set in runtime, from a `Initialized` event
    operations_count: Optional[int] = attr.ib(default=None)
    current_line_length: int = attr.ib(default=0)
    terminal_size: os.terminal_size = attr.ib(factory=shutil.get_terminal_size)
    results: List[SerializedTestResult] = attr.ib(factory=list)
    cassette_file_name: Optional[str] = attr.ib(default=None)
    junit_xml_file: Optional[str] = attr.ib(default=None)
    verbosity: int = attr.ib(default=0)
    code_sample_style: CodeSampleStyle = attr.ib(default=CodeSampleStyle.default())
    correlation_id_to_item_id: Dict = attr.ib(factory=dict)
