"""
Iolanta facet management.

This module contains a few functions which later will be refactored into
Iolanta - the generic metaverse/cyberspace browser.
"""
import operator
import pydoc
from dataclasses import dataclass
from typing import Protocol, Optional, Callable, Union

from documented import DocumentedError
from more_itertools import first
from rdflib.term import Node, URIRef
from urlpath import URL

from octadocs.octiron import Octiron


HTML = URIRef('https://html.spec.whatwg.org/')


@dataclass
class FacetNotCallable(DocumentedError):
    """
    Python facet not callable.

      - Import path: {self.path}
      - Object imported: {self.facet}

    The imported Python object is not a callable and thus cannot be used as a
    facet.
    """

    path: str
    facet: object


@dataclass
class FacetNotFound(DocumentedError):
    """
    Facet not found.

        Node: {self.node}
        Environment: {self.environment}

    We could not find a facet to display this node 😟
    """

    node: Node
    environment: URIRef


class PythonFacet(Protocol):
    def __call__(
        self,
        octiron: Octiron,
        node: Node,
        environment: URIRef,
    ) -> str:
        ...


def find_default_facet_iri_for_environment(octiron: Octiron, environment: URIRef):
    rows = octiron.query(
        '''
        SELECT * WHERE {
            ?environment iolanta:hasDefaultFacet ?facet .
        }
        ''',
        environment=environment,
    )

    facets = map(operator.itemgetter('facet'), rows)

    return first(facets, None)


def find_facet_iri(
    octiron: Octiron,
    environment: URIRef,
    node: Node,
) -> Optional[URIRef]:
    if not isinstance(node, URIRef):
        node = URIRef(node)

    rows = octiron.query(
        '''
        SELECT ?facet WHERE {
            ?node iolanta:facet ?facet .
            ?facet iolanta:supports ?environment .
        }
        ''',
        node=node,
        environment=environment,
    )

    facets = map(operator.itemgetter('facet'), rows)

    if facet := first(facets, None):
        return facet

    facet = find_default_facet_iri_for_environment(
        octiron=octiron,
        environment=environment,
    )

    if facet is None:
        raise FacetNotFound(
            node=node,
            environment=environment,
        )

    return facet


def resolve_facet(iri: URIRef) -> Callable[[Octiron, Node], str]:
    url = URL(str(iri))

    if url.scheme != 'python':
        raise Exception(
            'Octadocs only supports facets which are importable Python '
            'callables. The URLs of such facets must start with `python://`, '
            'which {url} does not comply to.'.format(
                url=url,
            )
        )

    facet = pydoc.locate(url.hostname)

    if not callable(facet):
        raise FacetNotCallable(
            path=url,
            facet=facet,
        )

    return facet


def render(
    node: Union[str, Node],
    octiron: Octiron,
    environment: URIRef = HTML,
) -> str:
    """Find an Iolanta facet for a node and render it."""
    facet_iri = find_facet_iri(
        octiron=octiron,
        environment=environment,
        node=node,
    )

    facet = resolve_facet(iri=facet_iri)

    return facet(
        octiron=octiron,
        iri=node,
    )
