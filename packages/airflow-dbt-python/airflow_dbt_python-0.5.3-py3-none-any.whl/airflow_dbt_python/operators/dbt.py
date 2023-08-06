from __future__ import annotations

import datetime as dt
from dataclasses import asdict, is_dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Any, Optional, Union

import dbt.flags as flags
from airflow import AirflowException
from airflow.models.baseoperator import BaseOperator
from airflow.models.xcom import XCOM_RETURN_KEY
from airflow.utils.decorators import apply_defaults
from dbt.contracts.results import RunExecutionResult, RunResult, agate
from dbt.logger import log_manager
from dbt.main import initialize_config_values, parse_args, track_run


class DbtBaseOperator(BaseOperator):
    """The basic Airflow dbt operator. Defines how to build an argument list and execute
        a dbt command. Does not set a command itself, subclasses should set it.

        Attributes:
        command: The dbt command to execute.
        project_dir: Directory for dbt to look for dbt_profile.yml. Defaults to current
    directory.
        profiles_dir: Directory for dbt to look for profiles.yml. Defaults to ~/.dbt.
        profile: Which profile to load. Overrides dbt_profile.yml.
        target: Which target to load for the given profile.
        vars: Supply variables to the project. Should be a YAML string. Overrides
    variables defined in dbt_profile.yml.
        log_cache_events: Flag to enable logging of cache events.
        bypass_cache: Flag to bypass the adapter-level cache of database state.

        Methods:
        execute: Executes a given dbt command.
        args_list: Produce a list of arguments for a dbt command.
        run_dbt_command: Runs the actual dbt command as defined by self.command.
        serializable_result: Turns a dbt result into a serializable object.
    """

    command: Optional[str] = None
    __dbt_args__ = [
        "project_dir",
        "profiles_dir",
        "profile",
        "target",
        "vars",
        "log_cache_events",
        "bypass_cache",
    ]

    @apply_defaults
    def __init__(
        self,
        positional_args: Optional[list[str]] = None,
        project_dir: Optional[Union[str, Path]] = None,
        profiles_dir: Optional[Union[str, Path]] = None,
        profile: Optional[str] = None,
        target: Optional[str] = None,
        vars: Optional[dict[str, str]] = None,
        log_cache_events: Optional[bool] = False,
        bypass_cache: Optional[bool] = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.positional_args = positional_args
        self.project_dir = project_dir
        self.profiles_dir = profiles_dir
        self.profile = profile
        self.target = target
        self.vars = vars
        self.log_cache_events = log_cache_events
        self.bypass_cache = bypass_cache

    def execute(self, context: dict):
        """Execute dbt command with prepared arguments"""
        if self.command is None:
            raise AirflowException("dbt command is not defined")

        args: list[Optional[str]] = [self.command]

        if self.positional_args is not None:
            args.extend(self.positional_args)
        args.extend(self.args_list())

        self.log.info("Running dbt %s with args %s", args[0], args[1:])

        with TemporaryDirectory(prefix="airflowtmp") as tmp_dir:
            with NamedTemporaryFile(dir=tmp_dir, mode="w+") as f:
                with log_manager.applicationbound():
                    log_manager.reset_handlers()
                    log_manager.set_path(tmp_dir)
                    # dbt logger writes to STDOUT and I haven't found a way
                    # to bubble up to the Airflow command logger. As a workaround,
                    # I set the output stream to a temporary file that is later
                    # read and logged using the command's logger.
                    log_manager.set_output_stream(f)
                    res, success = self.run_dbt_command(args)

                with open(f.name) as read_file:
                    for line in read_file:
                        self.log.info(line.rstrip())

        if self.do_xcom_push is True:
            # Some dbt operations use dataclasses for its results,
            # found in dbt.contracts.results. Each DbtBaseOperator
            # subclass should implement prepare_results to return a
            # serializable object
            res = self.serializable_result(res)

        if success is not True:
            if self.do_xcom_push is True and context.get("ti", None) is not None:
                self.xcom_push(context, key=XCOM_RETURN_KEY, value=res)
            raise AirflowException(f"dbt {args[0]} {args[1:]} failed")
        return res

    def args_list(self) -> list[str]:
        """Build a list of arguments to pass to dbt"""
        args = []
        for arg in self.__dbt_args__:
            value = getattr(self, arg, None)
            if value is None:
                continue

            if arg.startswith("dbt_"):
                arg = arg[4:]

            if not isinstance(value, bool) or value is True:
                flag = "--" + arg.replace("_", "-")
                args.append(flag)

            if isinstance(value, bool):
                continue
            elif any(isinstance(value, _type) for _type in (str, Path, int)):
                args.append(str(value))
            elif isinstance(value, list):
                args.extend(value)
            elif isinstance(value, dict):
                yaml_str = (
                    "{"
                    + ", ".join("{}: {}".format(k, v) for k, v in value.items())
                    + "}"
                )
                args.append(yaml_str)

        return args

    def run_dbt_command(self, args: list[Optional[str]]) -> tuple[RunResult, bool]:
        """Run a dbt command as implemented by a subclass"""
        try:
            parsed = parse_args(args)
        except Exception as exc:
            raise AirflowException("Failed to parse dbt arguments: {args}") from exc

        initialize_config_values(parsed)
        flags.set_from_args(parsed)
        parsed.cls.pre_init_hook(parsed)

        command = parsed.cls.from_args(args=parsed)
        results = None
        with track_run(command):
            results = command.run()

        success = command.interpret_results(results)
        return results, success

    def serializable_result(
        self, result: Optional[RunExecutionResult]
    ) -> Optional[dict[Any, Any]]:
        """
        Turn dbt's RunExecutionResult into a dict of only JSON-serializable types
        Each subclas may implement this method to return a dictionary of
        JSON-serializable types, the default XCom backend. If implementing
        custom XCom backends, this method may be overriden.
        """

        if result is None or is_dataclass(result) is False:
            return result
        return asdict(result, dict_factory=run_result_factory)


class DbtRunOperator(DbtBaseOperator):
    """Executes dbt run"""

    command = "run"

    __dbt_args__ = DbtBaseOperator.__dbt_args__ + [
        "full_refresh",
        "models",
        "fail_fast",
        "threads",
        "exclude",
        "selector",
        "state",
        "defer",
        "no_defer",
    ]

    def __init__(
        self,
        full_refresh: Optional[bool] = None,
        models: Optional[list[str]] = None,
        fail_fast: Optional[bool] = None,
        threads: Optional[int] = None,
        exclude: Optional[list[str]] = None,
        selector: Optional[str] = None,
        state: Optional[Union[str, Path]] = None,
        defer: Optional[bool] = None,
        no_defer: Optional[bool] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.full_refresh = full_refresh
        self.models = models
        self.fail_fast = fail_fast
        self.threads = threads
        self.exclude = exclude
        self.selector = selector
        self.state = state
        self.defer = defer
        self.no_defer = no_defer


class DbtSeedOperator(DbtBaseOperator):
    """Executes dbt seed"""

    command = "seed"

    __dbt_args__ = DbtBaseOperator.__dbt_args__ + [
        "full_refresh",
        "select",
        "show",
        "threads",
        "exclude",
        "selector",
        "state",
    ]

    def __init__(
        self,
        full_refresh: Optional[bool] = None,
        select: Optional[list[str]] = None,
        show: Optional[bool] = None,
        threads: Optional[int] = None,
        exclude: Optional[list[str]] = None,
        selector: Optional[str] = None,
        state: Optional[Union[str, Path]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.full_refresh = full_refresh
        self.select = select
        self.show = show
        self.threads = threads
        self.exclude = exclude
        self.selector = selector
        self.state = state


class DbtTestOperator(DbtBaseOperator):
    """Executes dbt test"""

    command = "test"

    __dbt_args__ = DbtBaseOperator.__dbt_args__ + [
        "data",
        "schema",
        "fail_fast",
        "models",
        "threads",
        "exclude",
        "selector",
        "state",
        "defer",
        "no_defer",
    ]

    def __init__(
        self,
        data: Optional[bool] = None,
        schema: Optional[bool] = None,
        models: Optional[list[str]] = None,
        fail_fast: Optional[bool] = None,
        threads: Optional[int] = None,
        exclude: Optional[list[str]] = None,
        selector: Optional[str] = None,
        state: Optional[Union[str, Path]] = None,
        defer: Optional[bool] = None,
        no_defer: Optional[bool] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.data = data
        self.schema = schema
        self.models = models
        self.fail_fast = fail_fast
        self.threads = threads
        self.exclude = exclude
        self.selector = selector
        self.state = state
        self.defer = defer
        self.no_defer = no_defer


class DbtCompileOperator(DbtBaseOperator):
    """Executes dbt compile"""

    command = "compile"

    __dbt_args__ = DbtBaseOperator.__dbt_args__ + [
        "parse_only",
        "full_refresh",
        "fail_fast",
        "threads",
        "models",
        "exclude",
        "selector",
        "state",
    ]

    def __init__(
        self,
        parse_only: Optional[bool] = None,
        full_refresh: Optional[bool] = None,
        models: Optional[list[str]] = None,
        fail_fast: Optional[bool] = None,
        threads: Optional[int] = None,
        exclude: Optional[list[str]] = None,
        selector: Optional[str] = None,
        state: Optional[Union[str, Path]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.parse_only = parse_only
        self.full_refresh = full_refresh
        self.models = models
        self.fail_fast = fail_fast
        self.threads = threads
        self.exclude = exclude
        self.selector = selector
        self.state = state


class DbtDepsOperator(DbtBaseOperator):
    """Executes dbt deps"""

    command = "deps"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class DbtCleanOperator(DbtBaseOperator):
    """Executes dbt clean"""

    command = "clean"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class DbtDebugOperator(DbtBaseOperator):
    """Execute dbt debug"""

    command = "debug"

    __dbt_args__ = DbtBaseOperator.__dbt_args__ + ["config_dir", "no_version_check"]

    def __init__(
        self,
        config_dir: Optional[bool] = None,
        no_version_check: Optional[bool] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.config_dir = config_dir
        self.no_version_check = no_version_check


class DbtSnapshotOperator(DbtBaseOperator):
    """Execute dbt snapshot"""

    command = "snapshot"

    __dbt_args__ = DbtBaseOperator.__dbt_args__ + [
        "select",
        "threads",
        "exclude",
        "selector",
        "state",
    ]

    def __init__(
        self,
        select: Optional[list[str]] = None,
        threads: Optional[int] = None,
        exclude: Optional[list[str]] = None,
        selector: Optional[str] = None,
        state: Optional[Union[str, Path]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.select = select
        self.threads = threads
        self.exclude = exclude
        self.selector = selector
        self.state = state


class DbtLsOperator(DbtBaseOperator):
    """Execute dbt list (or ls)"""

    command = "ls"

    __dbt_args__ = DbtBaseOperator.__dbt_args__ + [
        "resource_type",
        "select",
        "models",
        "exclude",
        "selector",
        "dbt_output",
    ]

    def __init__(
        self,
        resource_type: Optional[list[str]] = None,
        select: Optional[list[str]] = None,
        models: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
        selector: Optional[str] = None,
        dbt_output: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.resource_type = resource_type
        self.select = select
        self.models = models
        self.exclude = exclude
        self.selector = selector
        self.dbt_output = dbt_output


# Convinience alias
DbtListOperator = DbtLsOperator


class DbtRunOperationOperator(DbtBaseOperator):
    """Execute dbt run-operation"""

    command = "run-operation"

    __dbt_args__ = DbtBaseOperator.__dbt_args__ + [
        "args",
    ]

    def __init__(
        self,
        macro: str,
        args: Optional[dict[str, str]] = None,
        **kwargs,
    ) -> None:
        super().__init__(positional_args=[macro], **kwargs)
        self.args = args


def run_result_factory(data: list[tuple[Any, Any]]):
    """
    We need to handle dt.datetime and agate.table.Table.
    The rest of the types should already be JSON-serializable.
    """
    d = {}
    for key, val in data:
        if isinstance(val, dt.datetime):
            val = val.isoformat()
        elif isinstance(val, agate.table.Table):
            # agate Tables have a few print methods but they offer plain
            # text representations of the table which are not very JSON
            # friendly. There is a to_json method, but I don't think
            # sending the whole table in an XCOM is a good idea either.
            val = {
                k: v.__class__.__name__
                for k, v in zip(val._column_names, val._column_types)
            }
        d[key] = val
    return d
