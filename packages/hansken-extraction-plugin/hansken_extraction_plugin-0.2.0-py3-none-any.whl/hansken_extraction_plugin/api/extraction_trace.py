"""
This module contains the different Trace apis.

Note that there are a couple of different traces:
  * The ExtractionTrace and MetaExtractionTrace, which are offered to the process function.
  * ExtractionTraceBuilder, which is a trace that can be built; it does not exist in hansken yet, but it is added after
    building.
  * SearchTrace, which represents an immutable trace which is returned after searching for traces.
"""
from abc import ABC, abstractmethod
from io import BufferedReader
from typing import Any, Mapping, Union


class Tracelet:
    """
    A tracelet contains the values of a single fvt (Few Valued Type).

    A few valued type is a trace property type that is a collection of tracelets. A trace can contain multiple few
    valued types containing one or more tracelets. For example, the `trace.identity`` type may look like this::

        {emailAddress: 'interesting@notreally.com'},
        {firstName: 'piet'},
        {emailAddress: 'anotheremail@notreally.com'},

    The trace.identity few valued types contains three different tracelets.
    """

    def __init__(self, name: str, value: Mapping):
        """
        Initialize a tracelet.

        :param name: name or type of the tracelet. In the example this would be ``identity``.
        :param value: Mapping of keys to properties of this tracelet. In the example this could be
                      ``{emailAddress: 'anotheremail@notreally.com'}``.
        """
        self.name = name
        self.value = value


class ExtractionTraceBuilder(ABC):
    """
    ExtractionTrace that can be build.

    Represents child traces.
    """

    @abstractmethod
    def update(self, key_or_updates: Union[Mapping, str] = None, value: Any = None,
               data: Mapping[str, bytes] = None) -> 'ExtractionTraceBuilder':
        """
        Update or add metadata properties for this `.ExtractionTraceBuilder`.

        Can be used to update the name of the Trace represented by this builder,
        if not already set.

        :param key_or_updates: either a `str` (the metadata property to be
                               updated) or a mapping supplying both keys and values to be updated
        :param value: the value to update metadata property *key* to (used
                      only when *key_or_updates* is a `str`, an exception will be thrown
                      if *key_or_updates* is a mapping)
        :param data: a `dict` mapping data type / stream name to bytes to be
                     added to the trace
        :return: this `.ExtractionTraceBuilder`
        """

    @abstractmethod
    def add_tracelet(self, value: Tracelet) -> 'ExtractionTraceBuilder':
        """
        Add a `.Tracelet` to this `.ExtractionTraceBuilder`.

        :param value: the Tracelet to add
        :return: this `.ExtractionTraceBuilder`
        """

    @abstractmethod
    def child_builder(self, name: str = None) -> 'ExtractionTraceBuilder':
        """
        Create a new `.TraceBuilder` to build a child trace to the trace to be represented by this builder.

        .. note::
            Traces should be created and built in depth first order,
            parent before child (pre-order).

        :return: a `.TraceBuilder` set up to save a new trace as the child
                 trace of this builder
        """

    def add_data(self, stream: str, data: bytes) -> 'ExtractionTraceBuilder':
        """
        Add data to this trace as a named stream.

        :param stream: name of the data stream to be added
        :param data: data to be attached
        :return: this `.ExtractionTraceBuilder`
        """
        return self.update(data={stream: data})

    @abstractmethod
    def build(self) -> str:
        """
        Save the trace being built by this builder to remote.

        .. note::
            Building more than once will result in an error being raised.

        :return: the new trace' id
        """


class Trace(ABC):
    """All trace classes should be able to return values."""

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """
        Return metadata properties for this `.ExtractionTrace`.

        :param key: the metadata property to be retrieved
        :param default: value returned if property is not set
        :return: the value of the requested metadata property
        """


class SearchTrace(Trace):
    """SearchTraces represent traces returned when searching for traces."""

    @abstractmethod
    def open(self, stream: str = 'raw', offset: int = 0, size: int = None) -> BufferedReader:
        """
        Open a data stream of the data that is being processed.

        :param stream: data stream of trace to open. defaults to raw. other examples are html, text, etc.
        :param offset: byte offset to start the stream on
        :param size: the number of bytes to make available
        :return: a file-like object to read bytes from the named stream
        """


class MetaExtractionTrace(Trace):
    """
    MetaExtractionTraces contain only metadata.

    This class represenst traces during the extraction of an extraction plugin without a data stream.
    """

    @abstractmethod
    def update(self, key_or_updates: Union[Mapping, str] = None, value: Any = None,
               data: Mapping[str, bytes] = None) -> None:
        """
        Update or add metadata properties for this `.ExtractionTrace`.

        :param key_or_updates: either a `str` (the metadata property to be
                               updated) or a mapping supplying both keys and values to be updated
        :param value: the value to update metadata property *key* to (used
                      only when *key_or_updates* is a `str`, an exception will be thrown
                      if *key_or_updates* is a mapping)
        :param data: a `dict` mapping data type / stream name to bytes to be
                     added to the trace
        """

    @abstractmethod
    def add_tracelet(self, value: Tracelet) -> None:
        """
        Add a `.Tracelet` to this `.MetaExtractionTrace`.

        :param value: the Tracelet to add
        :return: this `.MetaExtractionTrace`
        """

    @abstractmethod
    def child_builder(self, name: str = None) -> ExtractionTraceBuilder:
        """
        Create a `.TraceBuilder` to build a trace to be saved as a child of this `.Trace`.

        A new trace will only be added to the index once explicitly saved (e.g.
        through `.TraceBuilder.build`).

        .. note::
            Traces should be created and built in depth first order,
            parent before child (pre-order).

        :param name: the name for the trace being built
        :return: a `.TraceBuilder` set up to create a child trace of this `.MetaExtractionTrace`
        """


class ExtractionTrace(MetaExtractionTrace):
    """Trace offered to be processed."""

    @abstractmethod
    def open(self, offset: int = 0, size: int = None) -> BufferedReader:
        """
        Open a data stream of the data that is being processed.

        :param offset: byte offset to start the stream on
        :param size: the number of bytes to make available
        :return: a file-like object to read bytes from the named stream
        """
