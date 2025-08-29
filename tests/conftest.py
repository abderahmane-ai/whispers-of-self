import sys
from pathlib import Path


def _ensure_project_root_on_path() -> None:
    root = Path(__file__).resolve().parents[1]
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


_ensure_project_root_on_path()


# Rich progress/animation for smoother test feedback and clear pass reporting
from typing import Any, Dict, List, Optional

import pytest

try:
    from rich.console import Console
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TextColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
    )
except Exception:  # pragma: no cover - fallback if rich unavailable at runtime
    Console = None  # type: ignore
    Progress = None  # type: ignore


_rich_state: Dict[str, Any] = {
    "console": None,
    "progress": None,
    "task_id": None,
    "total": 0,
    "completed": 0,
    "passed": [],  # type: List[str]
}


def _rich_enabled() -> bool:
    return Console is not None and Progress is not None


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: pytest.Session) -> None:
    if not _rich_enabled():
        return
    console = Console()
    _rich_state["console"] = console
    progress = Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold]Running tests[/bold]"),
        BarColumn(bar_width=None),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        transient=True,
        console=console,
        expand=True,
    )
    _rich_state["progress"] = progress
    progress.start()


def pytest_collection_finish(session: pytest.Session) -> None:
    if not _rich_enabled():
        return
    total = session.testscollected or 0
    _rich_state["total"] = total
    progress: Any = _rich_state.get("progress")
    if progress is not None and _rich_state.get("task_id") is None:
        task_id = progress.add_task("tests", total=total)
        _rich_state["task_id"] = task_id


def _advance_progress() -> None:
    if not _rich_enabled():
        return
    progress: Any = _rich_state.get("progress")
    task_id = _rich_state.get("task_id")
    if progress is not None and task_id is not None:
        progress.update(task_id, advance=1)
    _rich_state["completed"] = int(_rich_state.get("completed", 0)) + 1


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    # Advance on terminal outcomes to keep the bar smooth
    if report.when == "call" and report.passed:
        _advance_progress()
        if _rich_enabled():
            _rich_state["passed"].append(report.nodeid)
    elif report.when == "call" and report.failed:
        _advance_progress()
    elif report.when == "setup" and report.skipped:  # skip happens at setup
        _advance_progress()


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    # Stop progress if running
    if _rich_enabled():
        progress: Any = _rich_state.get("progress")
        if progress is not None:
            progress.stop()

        console: Any = _rich_state.get("console")
        if console is not None:
            passed: List[str] = list(_rich_state.get("passed", []))
            total: int = int(_rich_state.get("total", 0))
            completed: int = int(_rich_state.get("completed", 0))
            denom: int = total if total > 0 else completed

            # Brief, clear summary of which tests passed
            console.print("\n[bold green]✔ Tests passed:[/bold green] " f"{len(passed)}/{denom}")
            if passed:
                for nodeid in passed:
                    console.print(f"  [green]✔[/green] {nodeid}")

            # If something didn't complete (e.g., errors during setup), show a hint
            if completed < total:
                console.print(
                    f"[yellow]Note:[/yellow] Completed {completed}/{total} items (some may have errored before call phase)."
                )

