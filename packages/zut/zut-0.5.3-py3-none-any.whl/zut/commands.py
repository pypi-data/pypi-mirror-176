"""
Add and execute commands easily, based on argparse.
Usefull for non-Django applications.
For Django applications, use including command management instead.
"""
from __future__ import annotations
import logging, sys, argparse
from types import CodeType, FunctionType, ModuleType
from pathlib import Path
from importlib import import_module
from importlib.util import find_spec
from .format import RED, format_help_text, format_description_text

logger = logging.getLogger(__name__)


def command(add_arguments: FunctionType = None, doc: str = None, name: str = None):
    """
    A decorator to define options for command functions.
    """
    def decorator(func):
        if name is not None:
            func.command_name = name
        if doc is not None:
            func.__doc__ = doc
        if add_arguments is not None:
            func.add_arguments = add_arguments
        
        return func
    
    return decorator


def add_func_command(parser: argparse.ArgumentParser, func: FunctionType, name: str = None, add_arguments_func: FunctionType = None):
    """
    Add function `func` as subcommand `name` of `parser`.
    """
    # Determine help strings (from function docstring)
    description = format_description_text(func.__doc__)
    help = format_help_text(func.__doc__)

    # Determine command options
    if name is None:
        name = getattr(func, "command_name", func.__name__)

    if add_arguments_func is None:
        add_arguments_func = _get_add_arguments(func)

    # Determine command parser object
    subparsers = get_subparsers(parser)
    cmdparser = subparsers.add_parser(name, help=help, description=description, formatter_class=argparse.RawTextHelpFormatter)

    # Add command
    if add_arguments_func:
        add_arguments_func(cmdparser)

    if "func" in cmdparser._defaults:
        raise ValueError(f"{name} command already has a registered func")
    cmdparser.set_defaults(func=func)
    
    return cmdparser


def add_module_command(parser: argparse.ArgumentParser, module: str|ModuleType, name: str = None):
    """
    Add command from functions in a module. By default, command function is expected to be named "handler"
    and arguments definition function is expected to be named "add_arguments".
    """
    if not isinstance(module, ModuleType):
        module = import_module(module)

    func = getattr(module, "handle")

    if name is None:
        name = getattr(func, "command_name", None)
        if name is None:
            name = module.__name__.split(".")[-1]
    
    add_arguments_func = getattr(module, "add_arguments", None)
    if not add_arguments_func:
        add_arguments_func = _get_add_arguments(func)
    
    add_func_command(parser, func, name=name, add_arguments_func=add_arguments_func)


def add_package_commands(parser: argparse.ArgumentParser, package: str):
    package_spec = find_spec(package)
    if not package_spec:
        raise KeyError(f"package not found: {package}")
    if not package_spec.origin:
        raise KeyError(f"not a package: {package} (did you forget __init__.py ?)")
    package_path = Path(package_spec.origin).parent
    
    for module_path in package_path.iterdir():
        if module_path.is_dir() or module_path.name.startswith("_") or not module_path.name.endswith(".py"):
            continue

        module = module_path.stem
        add_module_command(parser, f"{package}.{module}")


def add_object_commands(parser: argparse.ArgumentParser, instance: any, exclude = []):
    for name in dir(instance):
        if exclude and name in exclude:
            continue

        if name.startswith("_") or name in ["exec"]:
            continue

        func = getattr(instance, name)
        if not callable(func):
            continue

        add_func_command(parser, func, add_arguments_func=getattr(instance, f"_{name}_add_arguments", None))


def run_command(parser: argparse.ArgumentParser, *args, default_func: FunctionType = None, default_add_arguments_func: FunctionType = None):
    """
    Run the command-line application, returning command result.
    """    
    args, unknown = parser.parse_known_args(*args)
    args = vars(args)
    func = args.pop('func', None)

    if func:
        if unknown:
            parser.print_usage(file=sys.stderr)
            print(f"{parser.prog}: error: unrecognized arguments: {' '.join(unknown)}", file=sys.stderr)
            return 2

    elif default_func:
        default_parser = argparse.ArgumentParser(prog=f"{parser.prog} (default)")

        if not default_add_arguments_func:
            default_add_arguments_func = _get_add_arguments(default_func)
            if default_add_arguments_func:
                default_add_arguments_func(default_parser)

        args = vars(default_parser.parse_args(*args))
        func = default_func

    else:
        print(RED % "missing command name", file=sys.stderr)
        return 2

    return func(**args)


def exec_command(parser: argparse.ArgumentParser, *args, default_func: FunctionType = None, default_add_arguments_func: FunctionType = None):
    """
    Run the command-line application and exit with appropriate return code.
    """
    r = run_command(*args, parser=parser, default_func=default_func, default_add_arguments_func=default_add_arguments_func)
    if not isinstance(r, int):
        r = 0 if r is None or r is True else 1
    sys.exit(r)


def call_command(cmd: str, *args: any, parser: argparse.ArgumentParser = None):
    if parser is None:
        #TODO/ROADMAP: better detection of default parser?
        from __main__ import parser

    cmd_with_args = [cmd] + [str(arg) for arg in args]
    return run_command(parser, *cmd_with_args)


def _get_add_arguments(func: FunctionType) -> FunctionType:
    """
    Return the `add_arguments` function, defined as a function attribute, or nested in `func`.
    Return `None` if inexistant.
    """
    add_arguments_func = getattr(func, 'add_arguments', None)

    if add_arguments_func:
        return add_arguments_func

    consts = func.__code__.co_consts
    for item in consts:
        if isinstance(item, CodeType) and item.co_name == "add_arguments":
            try:
                return FunctionType(item, globals())
            except:
                logger.exception(f"cannot use `add_arguments` nested in function `{func.__name__}`")
                return None


def get_subparsers(parser: argparse.ArgumentParser) -> argparse._SubParsersAction:
    """
    Get or create the subparsers object associated with the given parser.
    """
    if parser._subparsers is not None:
        return next(filter(lambda action: isinstance(action, argparse._SubParsersAction), parser._subparsers._actions))
    else:
        return parser.add_subparsers()
