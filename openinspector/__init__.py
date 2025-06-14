from importlib import metadata

try:
    __version__: str = metadata.version("openinspector")
except metadata.PackageNotFoundError:  # type: ignore[attr-defined]
    __version__ = "0.1.0"

# Public re-exports
from .config import settings  # noqa: F401
from .client import OpenInspectorClient  # noqa: F401

# Initialise LangSmith tracing (if configured)
try:
    import langsmith
    langsmith.tracing.enable_tracing()
except Exception:
    # Tracing is optional – silently continue when unsupported
    pass 