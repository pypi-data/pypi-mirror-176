from __future__ import annotations
import sys, inspect, logging
from pathlib import Path
from .logging import configure_logging
from .network import configure_proxy

def get_venv() -> Path|None:
    """
    Return the path to the virtual environment if Python runs inside a virtual environment, None otherwise.
    """
    base_prefix = getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
    if base_prefix == sys.prefix:
        return None
    return Path(sys.prefix)


_cache = {}


def configure_env(level: int|str = None, default_level: int|str = None, nocount: bool = False, logging_config: dict = None, configure_proxy_func = None, **configure_proxy_options) -> Path:
    """
    Load `.env` file into environment variables, configure logging and proxy, and return a `BASE_DIR` from which other paths in your project may be built.

    This should be called in the file `__init__.py` or `settings.py` of your project package.

    If your package is installed as a Python library (that is, if it is in a directory named `dist-packages` or `site-packages`), `BASE_DIR` will be the current working directory.
    Otherwise, `BASE_DIR` will be your package container.

    File `.env` will be loaded from the current working directory if available, otherwise from `BASE_DIR` is available.
    """
    if "BASE_DIR" in _cache:
        logger = logging.getLogger(__name__)
        logger.debug("already configured previously (%s)", _cache["configured_env"])
        return _cache["BASE_DIR"]

    caller_filename = inspect.stack()[1].filename 

    BASE_DIR = Path(caller_filename).resolve().parent.parent
    if BASE_DIR.name in ["dist-packages", "site-packages"]:
        BASE_DIR = Path.cwd()

    dotenv = Path.cwd().joinpath(".env")
    if not dotenv.exists():
        dotenv = BASE_DIR.joinpath(".env")
        if not dotenv.exists():
            dotenv = None
    
    _cache["configured_env"] = "BASE_DIR: %s, dotenv: %s" % (BASE_DIR, dotenv)

    if dotenv:
        from dotenv import load_dotenv
        load_dotenv(dotenv)

    # Configure logging
    configure_logging(level=level, default_level=default_level, nocount=nocount, config=logging_config)

    # Configure proxy
    if configure_proxy_func:
        _cache["configured_env"] += ", configure_proxy_func: %s" % configure_proxy_func.__name__
    else:
        configure_proxy_func = configure_proxy
    configure_proxy_func(**configure_proxy_options)

    # Report for debug
    logger = logging.getLogger(__name__)
    logger.debug("configured BASE_DIR: %s, dotenv: %s", BASE_DIR, dotenv)

    _cache["BASE_DIR"] = BASE_DIR
    return BASE_DIR
