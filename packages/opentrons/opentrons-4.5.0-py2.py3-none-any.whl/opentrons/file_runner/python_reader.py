"""Python file reading and parsing."""
import importlib.util
from types import ModuleType

from opentrons.protocol_api_experimental import ProtocolContext
from .protocol_file import ProtocolFile


class PythonProtocol:
    """A thin wrapper around the imported Python module."""

    def __init__(self, protocol_module: ModuleType) -> None:
        """Wrap the passed in protocol module."""
        self._protocol_module = protocol_module

    def run(self, context: ProtocolContext) -> None:
        """Call the protocol module's run method."""
        return self._protocol_module.run(context)  # type: ignore[attr-defined]


class PythonFileReader:
    """A reader for Python protocol files.

    Gets a Python protocol's metadata (TODO) and run method.
    """

    @staticmethod
    def read(protocol_file: ProtocolFile) -> PythonProtocol:
        """Read a Python protocol as a `import`ed Python module."""
        # TODO(mc, 2021-06-30): better module name logic
        spec = importlib.util.spec_from_file_location(
            name="protocol",
            location=protocol_file.file_path,
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]

        # TODO(mc, 2021-06-30): actually check that this module shape is good
        return PythonProtocol(protocol_module=module)
