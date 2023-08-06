"""
Implementation of the api using ``Hansken.py``.

All api calls are translated to ``Hansken.py`` calls.
"""
from io import BufferedReader
from typing import Any, Callable, cast, Dict, List, Tuple

from hansken.abstract_trace import AbstractTrace
from hansken.tool import run
from hansken.trace import TraceBuilder
from logbook import Logger  # type: ignore

from hansken_extraction_plugin.api.data_context import DataContext
from hansken_extraction_plugin.api.extraction_plugin import BaseExtractionPlugin, DeferredExtractionPlugin, \
    ExtractionPlugin, MetaExtractionPlugin
from hansken_extraction_plugin.api.extraction_trace import ExtractionTrace, ExtractionTraceBuilder, SearchTrace, \
    Tracelet
from hansken_extraction_plugin.api.search_result import SearchResult
from hansken_extraction_plugin.api.trace_searcher import TraceSearcher
from hansken_extraction_plugin.api.transformation import Transformation
from hansken_extraction_plugin.runtime.common import validate_update_arguments

log = Logger(__name__)


class HanskenPyExtractionTraceBuilder(ExtractionTraceBuilder):
    """
    Helper class that wraps a trace from ``Hansken.py`` in a ExtractionTraceBuilder.

    Delegates all calls to the wrapped hansken py trace builder.
    """

    def __init__(self, builder: TraceBuilder):
        """
        Initialize a TraceBuilder.

        :param builder: hansken.py tracebuilder. All calls are delegated to this object.
        """
        self._hanskenpy_trace_builder = builder
        self._tracelet_properties: List[Tracelet] = []
        self._transformations: Dict[str, List[Transformation]] = {}

    def update(self, key_or_updates=None, value=None, data=None) -> ExtractionTraceBuilder:
        """Override :meth: `ExtractionTrace.get`."""
        if data is not None:
            for stream_name in data:
                self._hanskenpy_trace_builder.add_data(stream=stream_name, data=data[stream_name])

        if key_or_updates is not None or value is not None:
            validate_update_arguments(key_or_updates, value)
            self._hanskenpy_trace_builder.update(key_or_updates, value)

        return self

    def add_tracelet(self, tracelet: Tracelet) -> 'ExtractionTraceBuilder':
        """
        Override :meth: `ExtractionTraceBuilder.add_tracelet`.

        Log an error because ``Hansken.py`` does not yet support adding tracelets.
        """
        # TODO HANSKEN-15372 Extraction plugin tracelet support FVT via REST API
        log.error(f"PluginRunner doesn't support add_tracelet over REST API, Tracelet is dropped {tracelet.name}")
        if tracelet is None:
            raise ValueError('tracelet is required')
        self._tracelet_properties.append(tracelet)
        return self

    def add_transformation(self, data_type: str, transformation: Transformation) -> 'ExtractionTraceBuilder':
        """
        Override :meth: `ExtractionTraceBuilder.add_transformation`.

        Log an error because ``Hansken.py`` does not yet support adding transformations.
        """
        # TODO HBACKLOG-399 Add datadescriptors to REST API
        log.error("PluginRunner doesn't support add_transformation over REST API, Transformation is dropped")
        if not data_type:
            raise ValueError('data_type is required')
        if transformation is None:
            raise ValueError('transformation is required')
        self._transformations.setdefault(data_type, []).append(transformation)
        return self

    def child_builder(self, name: str = None) -> 'ExtractionTraceBuilder':
        """Override :meth: `ExtractionTraceBuilder.child_builder`."""
        return HanskenPyExtractionTraceBuilder(self._hanskenpy_trace_builder.child_builder(name))

    def build(self) -> str:
        """Override :meth: `ExtractionTraceBuilder.get`."""
        return self._hanskenpy_trace_builder.build()


class HanskenPyExtractionTrace(ExtractionTrace):
    """
    Helper class that wraps a trace from ``Hansken.py`` in a ExtractionTrace.

    We delegate all calls of the abstract class Mapping to the ``Hansken.py`` trace,
    since ``Hansken.py`` does a lot of tricks to get things working.
    """

    def __init__(self, trace: AbstractTrace, data_context: DataContext):
        """
        Initialize an ExtractionTrace.

        :param trace: all mapping calls are delegated to this ``Hansken.py`` trace
        :param data_context: ``Hansken.py`` data_context used to perform rest calls
        """
        self._hanskenpy_trace = trace
        self._new_properties: Dict[str, Any] = {}
        self._tracelet_properties: List[Tracelet] = []
        self._transformations: Dict[str, List[Transformation]] = {}
        self._data_context = data_context

    def update(self, key_or_updates=None, value=None, data=None) -> None:
        """Override :meth: `ExtractionTrace.update`."""
        if data is not None:
            self._hanskenpy_trace.update(data=data)

        if key_or_updates is not None or value is not None:
            validate_update_arguments(key_or_updates, value)
            self._hanskenpy_trace.update(key_or_updates, value, overwrite=True)
            updates = key_or_updates

            if isinstance(key_or_updates, str):
                updates = {key_or_updates: value}

            # update does not add the new properties to the trace _source, so
            # keep track of them here, so that we can return them when someone calls get(new_property)
            for name, value in updates.items():
                self._new_properties[name] = value

    def add_tracelet(self, tracelet: Tracelet) -> None:
        """
        Override :meth: `ExtractionTrace.add_tracelet`.

        Log an error because ``Hansken.py`` does not yet support adding tracelets.
        """
        # TODO HANSKEN-15372 Extraction plugin tracelet support FVT via REST API
        log.error(f"PluginRunner doesn't support add_tracelet over REST API, Tracelet is dropped {tracelet.name}")
        if tracelet is None:
            raise ValueError('tracelet is required')
        self._tracelet_properties.append(tracelet)

    def add_transformation(self, data_type: str, transformation: Transformation) -> None:
        """
        Override :meth: `ExtractionTrace.add_transformation`.

        Log an error because ``Hansken.py`` does not yet support adding transformations.
        """
        # TODO HBACKLOG-399 Add datadescriptors to REST API
        log.error("PluginRunner doesn't support add_transformation over REST API, Transformation is dropped")
        if not data_type:
            raise ValueError('data_type is required')
        if transformation is None:
            raise ValueError('transformation is required')
        self._transformations.setdefault(data_type, []).append(transformation)

    def open(self, offset=0, size=None) -> BufferedReader:
        """Override :meth: `ExtractionTrace.open`."""
        return self._hanskenpy_trace.open(stream=self._data_context.data_type(), offset=offset, size=size)

    def child_builder(self, name: str = None) -> ExtractionTraceBuilder:
        """Override :meth: `ExtractionTrace.child_builder`."""
        return HanskenPyExtractionTraceBuilder(self._hanskenpy_trace.child_builder(name))

    def get(self, key, default=None) -> Any:
        """Override :meth: `Trace.get`."""
        return self._new_properties[key] if key in self._new_properties else self._hanskenpy_trace.get(key, default)


class HanskenPySearchTrace(SearchTrace):
    """SearchTrace implementation that forwards all calls to a ``Hansken.py`` trace."""

    def __init__(self, trace: AbstractTrace):
        """
        Initialize a SearchTrace.

        :param trace: ``Hansken.py`` trace to forward all calls to
        """
        self._hanskenpy_trace = trace

    def open(self, stream='raw', offset=0, size=None) -> BufferedReader:
        """Override :meth: `SearchTrace.open`."""
        return self._hanskenpy_trace.open(stream=stream, offset=offset, size=size)

    def get(self, key, default=None):
        """Override :meth: `Trace.get`."""
        return self._hanskenpy_trace.get(key, default)


class HanskenPySearchResult(SearchResult):
    """SearchResult implementation that wraps the searchresult from ``Hansken.py`` so sdk SearchTraces are returned."""

    def __init__(self, result):
        """
        Initialize a SearchResult.

        :param result: ``Hansken.py`` search result to wrap
        """
        self._result = result

    def __iter__(self):
        return map(HanskenPySearchTrace, self._result.__iter__())

    def total_results(self) -> int:
        """Override :meth: `SearchResult.total_results`."""
        return self._result.num_results

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Override :meth: `SearchResult.close`.

        The provided hansken py search result needs to be closed explicitly.
        """
        self._result.close()


class HanskenPyTraceSearcher(TraceSearcher):
    """TraceSearcher implementation that forwards search requests to ``Hansken.py``."""

    def __init__(self, h_py_context):
        """
        Initialize a TraceSearcher.

        :param h_py_context: ``Hansken.py`` ExtractionContext to perform the required REST calls
        """
        self.h_py_context = h_py_context

    def search(self, query: str, count: int) -> SearchResult:
        """Override :meth: `TraceSearcher.search`."""
        return HanskenPySearchResult(self.h_py_context.search(query=query, count=count))


class _PluginRunner:
    """Helper class that allows an Extraction Plugin to be executed with ``Hansken.py``."""

    def __init__(self, extraction_plugin_class: Callable[[], BaseExtractionPlugin]):
        """
        Initialize a PluginRunner.

        :param extraction_plugin_class: callable returning an instance of the extraction plugin to run
        """
        self._extraction_plugin_class = extraction_plugin_class

    def run(self, context):
        """
        Run the extraction plugin.

        :param context: most plugin calls will be forwarded to this ``Hansken.py`` extraction data_context.
        """
        log.info('PluginRunner is running plugin class {}', self._extraction_plugin_class.__name__)
        plugin = self._extraction_plugin_class()

        query, data_stream_type = _split_matcher(plugin.plugin_info().matcher)
        with context:
            for trace in context.search(query):
                sdk_context = DataContext(data_size=trace.get('data.{}.size'.format(data_stream_type)),
                                          data_type=data_stream_type)
                if isinstance(plugin, DeferredExtractionPlugin):
                    searcher = HanskenPyTraceSearcher(context)
                    cast(DeferredExtractionPlugin, plugin).process(HanskenPyExtractionTrace(trace, sdk_context),
                                                                   sdk_context, searcher)
                if isinstance(plugin, ExtractionPlugin):
                    cast(ExtractionPlugin, plugin).process(HanskenPyExtractionTrace(trace, sdk_context), sdk_context)
                if isinstance(plugin, MetaExtractionPlugin):
                    cast(MetaExtractionPlugin, plugin).process(HanskenPyExtractionTrace(trace, sdk_context))


def _split_matcher(matcher: str) -> Tuple[str, str]:
    """
    Split a matcher string into HQL and the data stream type portions.

    It requires the data stream type to be at the END of the string.
    Example::

        A AND B AND C AND $data.type=raw

    :param matcher: the HQL matcher of this plugin + the $data.type suffix
    :return: A tuple containing the HQL query and the type value of the '$data.type=value' argument
    """
    data_type_prefix = 'and $data.type='
    error_message = 'a matcher should end with "$data.type=value"'
    matcher = matcher.strip()

    # starts with $data.type or contains more than 1
    if matcher.lower().count(data_type_prefix) != 1:
        raise TypeError(error_message)

    index = matcher.lower().index(data_type_prefix)

    # $data.type not at end of line. the substring 'and $data.type=value' should contain exactly 1 space.
    if matcher[index:].count(' ') != 1:
        raise TypeError(error_message)

    query = matcher[:index]
    data_stream_type = matcher[index + len(data_type_prefix):]
    return query, data_stream_type


def run_with_hanskenpy(extraction_plugin_class: Callable[[], BaseExtractionPlugin], **defaults):
    """
    Run an Extraction Plugin as a script on a specific project, using ``Hansken.py``.

    An Extraction Plugin as scripts is executed against a Hansken server, on a project that already has been extracted.

    extraction_plugin_class: Class of the extraction plugin implementation
    """
    runner = _PluginRunner(extraction_plugin_class)
    run(with_context=runner.run, **defaults)
