import traceback
from ast import List
from concurrent.futures import ThreadPoolExecutor
from email.generator import Generator

from rich.progress import Progress, SpinnerColumn, TaskID, TextColumn


class BaseError(Exception):
    pass


def new_progress():
    from sarina.core import console

    return Progress(
        SpinnerColumn(),
        TextColumn(
            "[blue]{task.description}:[/blue] {task.fields[message]}",
            justify="left",
        ),
        console=console,
    )


def run_task(description: str, g: Generator, progress: Progress, raise_exc=False):
    task_id = progress.add_task(description, message="", start=True, total=1)
    last_message = ""
    try:
        while True:
            step = next(g)
            last_message = step
            progress.update(task_id, message=step)
    except StopIteration as e:
        progress.update(task_id, message=f"{last_message} [green]OK")
        progress.advance(task_id, 1)
        return e.value
    except BaseError as e:
        progress.update(
            task_id,
            message=f"{last_message} [red]Fail[/red] [deep_pink4]{str(e)}[/deep_pink4]",
        )
        progress.advance(task_id, 1)
        if raise_exc:
            raise
        return None
    except Exception as e:
        progress.console.error(traceback.format_exc())
        progress.update(
            task_id,
            message=f"{last_message} [red]Fail[/red] [deep_pink4]{str(e)}[/deep_pink4]",
        )
        progress.advance(task_id, 1)
        if raise_exc:
            raise
        return None


def with_prefix(prefix: str, g: Generator, style="light_slate_grey") -> Generator:
    yield prefix
    for m in g:
        if style:
            yield f"{prefix} [{style}]{m}[/{style}]"
        else:
            yield f"{prefix} {m}"


class TaskPool(ThreadPoolExecutor):
    progress: Progress
    _futures: List

    def __init__(self, progress: Progress, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progress = progress
        self._futures = []

    def submit(self, description: str, t: Generator):
        r = super().submit(
            run_task, description, t, progress=self.progress, raise_exc=True
        )
        self._futures.append(r)
        return r

    @property
    def results(self):
        return [f.result() for f in self._futures]

    @property
    def exceptions(self):
        return [f.exception for f in self._futures]
