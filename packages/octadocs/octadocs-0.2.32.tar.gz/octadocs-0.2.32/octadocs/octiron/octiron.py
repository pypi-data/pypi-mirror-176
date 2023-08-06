import copy
import logging
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import reduce
from pathlib import Path
from types import MappingProxyType
from typing import Any, Dict, Iterable, Optional, Set

import funcy
import rdflib
from rdflib.term import Node

from iolanta.context import merge
from iolanta.loaders.local_file import IsAContext, ParserNotFound
from iolanta.models import LDContext
from iolanta.namespaces import LOCAL
from iolanta.shortcuts import as_quad_stream
from ldflex import LDFlex
from octadocs.conversions import triples_to_quads
from octadocs.describe_documentation_page import describe_documentation_page
from octadocs.octiron.context_loaders import (
    context_from_json,
    context_from_yaml,
)
from octadocs.octiron.inference import (
    apply_inference_owlrl,
    apply_inference_sparql,
)
from octadocs.query import _format_query_bindings
from octadocs.storage import save_graph
from octadocs.types import DEFAULT_NAMESPACES
from octadocs.types import LOCAL as local
from octadocs.types import Context, QueryResult
from rdflib import ConjunctiveGraph
from rdflib.plugins.sparql.processor import SPARQLResult
from typer import Typer
from urlpath import URL

if sys.version_info >= (3, 8):
    from functools import cached_property  # noqa
else:
    from backports.cached_property import cached_property  # noqa: WPS433,WPS440

logger = logging.getLogger(__name__)

CONTEXT_FORMATS = MappingProxyType({
    'context.json': context_from_json,
    'context.yaml': context_from_yaml,
})


class CacheStatus(Enum):
    """Cache condition of a file."""

    NOT_CACHED = auto()
    UP_TO_DATE = auto()
    EXPIRED = auto()


@dataclass
class Octiron:  # noqa: WPS214
    """
    Convert a lump of goo and data into a semantic graph.

    I believe that this class should be transformed into `Iolanta` class, and
    factored out of `octadocs` application into its own package.
    """

    root_directory: Path
    language: str
    custom_namespaces: Dict[str, rdflib.Namespace] = field(default_factory=dict)
    last_modified_timestamp_per_file: Dict[rdflib.URIRef, float] = field(
        default_factory=dict,
        metadata={
            '__doc__': 'Time when every file was last imported into the graph.',
        },
    )
    root_context: Optional[LDContext] = None
    cli: Dict[str, Typer] = field(default_factory=dict)

    @cached_property
    def namespaces(self):
        """
        Join the provided custom namespaces with the defaults.

        Returns all namespaces registered with this Octiron instance.
        """
        namespaces = dict(DEFAULT_NAMESPACES)
        namespaces.update(self.custom_namespaces)

        return namespaces

    @cached_property
    def graph(self) -> rdflib.ConjunctiveGraph:
        """Generate and instantiate the RDFLib graph instance."""
        conjunctive_graph = ConjunctiveGraph(
            identifier=LOCAL.term('_inference'),
        )

        for short_name, namespace in self.namespaces.items():
            conjunctive_graph.bind(short_name, namespace)

        return conjunctive_graph

    def get_context_per_directory(
        self,
        directory: Path,
    ) -> Context:
        """Find context file per disk directory."""
        return reduce(
            merge,  # type: ignore
            map(
                self._get_context_file,
                reversed(list(self._find_context_files(directory))),
            ),
            self.root_context or {},
        )

    def create_file_cache_status(
        self,
        local_iri: rdflib.URIRef,
        last_modification_timestamp_on_disk: float,
    ) -> CacheStatus:
        """Determine caching status of a file."""
        cached_modification_time = self.last_modified_timestamp_per_file.get(
            local_iri,
        )

        if cached_modification_time is None:
            return CacheStatus.NOT_CACHED

        elif cached_modification_time < last_modification_timestamp_on_disk:
            return CacheStatus.EXPIRED

        return CacheStatus.UP_TO_DATE

    def clear_named_graph(self, local_iri: rdflib.URIRef) -> None:
        """Remove all triples in the specified named graph."""
        # Ugly formatting is used because of:
        #   https://github.com/RDFLib/rdflib/issues/1277
        self.graph.update(f'CLEAR GRAPH <{local_iri}>')

    def update_from_file(  # noqa: WPS210
        self,
        path: Path,
        local_iri: rdflib.URIRef,
        named_contexts: Optional[Dict[str, Any]] = None,
        global_url: Optional[str] = None,
        skip_file_if_not_importable: bool = True,
    ) -> None:
        """Update the graph from file determined by given path."""
        # Create a shorter (printable) version of the path for logging messages.
        try:
            relative_path = path.relative_to(self.root_directory)
        except ValueError:
            relative_path = path

        file_last_modification_time = path.stat().st_mtime

        cache_status = self.create_file_cache_status(
            local_iri=local_iri,
            last_modification_timestamp_on_disk=file_last_modification_time,
        )

        if cache_status == CacheStatus.UP_TO_DATE:
            logger.info('Skipping %s (cached and up to date)', relative_path)
            return

        elif cache_status == CacheStatus.EXPIRED:
            self.clear_named_graph(local_iri)

        try:
            quads = as_quad_stream(
                url=URL(f'file://{path}'),
                iri=local_iri,
                default_context=copy.deepcopy(self.root_context),
                root_directory=self.root_directory,
                named_contexts=named_contexts,
            )
        except ParserNotFound:
            if skip_file_if_not_importable:
                logger.info(
                    'Cannot import %s because no loader was found.',
                    path,
                )
                return

            raise

        except IsAContext:
            logger.info('Cannot parse a context, sorry')
            return

        self.graph.addN(quads)

        triples = describe_documentation_page(
            iri=local_iri,
            path=path,
            docs_dir=self.root_directory,
        )

        quads = triples_to_quads(
            triples=triples,
            graph=local.fs,
        )

        self.graph.addN(quads)

        # Store the file last modification time
        self.last_modified_timestamp_per_file[local_iri] = (
            file_last_modification_time
        )

    def _legacy_get_quads(
        self,
        cache_status,
        context,
        global_url,
        loader_class,
        local_iri,
        named_contexts,
        path,
        relative_path,
    ):
        """Legacy mechanism to convert a file into quad stream."""
        logger.info(
            'Importing %s via %s (%s)',
            relative_path,
            loader_class.__name__,
            'not cached before' if (
                cache_status == CacheStatus.NOT_CACHED
            ) else 'cached but expired',
        )

        loader_instance = loader_class(
            path=path,
            context=context,
            local_iri=local_iri,
            global_url=global_url,
            named_contexts=named_contexts,
        )

        triples = loader_instance.stream()
        return triples_to_quads(triples=triples, graph=local_iri)

    def apply_inference(self) -> None:  # noqa: WPS213
        """Apply inference rules after graph has been updated from files."""
        apply_inference_owlrl(graph=self.graph)

        sparql_inference_applied = apply_inference_sparql(
            inference_directory=self.root_directory.parent / 'inference',
            graph=self.graph,
        )

        self.graph.update('''
        INSERT {
            GRAPH <local:inference/page-facet/> {
                ?page octa:template ?template .
            }
        } WHERE {
            ?page iolanta:facet [
                a octa:PageFacet ;
                iolanta:supports octa: ;
                octa:template ?template
            ] .
        }
        ''')

        if sparql_inference_applied:
            # Changes made by SPARQL queries might require another pass of OWL RL
            apply_inference_owlrl(graph=self.graph)

    def _find_context_files(self, directory: Path) -> Iterable[Path]:
        """
        Find all context files relevant to particular directory.

        Files are ordered from the deepest to the upmost.
        """
        for context_directory in (directory, *directory.parents):
            for filename in CONTEXT_FORMATS.keys():
                context_path = context_directory / filename

                if context_path.is_file():
                    yield context_path

            if context_directory == self.root_directory:
                return

    def _get_context_file(self, path: Path) -> Context:
        """Read and return context file by path."""
        logger.info('Loading context: %s', path)
        context_loader = CONTEXT_FORMATS[path.name]
        return context_loader(path)

    @cached_property
    def ldflex(self) -> LDFlex:
        """Construct LDFlex instance."""
        return LDFlex(self.graph)

    def query(
        self,
        query_text: str,
        **kwargs: str,
    ) -> QueryResult:
        """Run SPARQL SELECT, CONSTRUCT, or ASK query."""
        sparql_result: SPARQLResult = self.graph.query(
            query_text,
            initBindings=kwargs,
        )

        if sparql_result.askAnswer is not None:
            return sparql_result.askAnswer

        if sparql_result.graph is not None:
            graph: rdflib.Graph = sparql_result.graph
            for prefix, namespace in self.graph.namespaces():
                graph.bind(prefix, namespace)

            return graph

        return _format_query_bindings(sparql_result.bindings)

    def save_graph_to_cache(self):
        """Pickle the graph to reuse it in CLI and other tools."""
        save_graph(
            graph=self.graph,
            path=self.root_directory.parent / '.cache/octadocs',
        )
        logger.info('Saved graph to disk for CLI to use.')

    @cached_property
    def debugging_nodes(self) -> Set[Node]:
        return set(
            funcy.pluck(
                'node',
                self.query('SELECT * WHERE { ?node octa:debug true }'),
            ),
        )

    def is_debug_mode(self, node: Node) -> bool:
        return node in self.debugging_nodes
