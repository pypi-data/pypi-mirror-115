from dominate.tags import a
from more_itertools import first
from rdflib import URIRef

from octadocs.octiron import Octiron


def link(octiron: Octiron, iri: URIRef) -> a:
    """Default facet to draw a link to something in HTML environment."""
    descriptions = octiron.query(
        '''
        SELECT * WHERE {
            ?page
                octa:url ?url ;
                octa:title ?label .
        } ORDER BY ?label LIMIT 1
        ''',
        page=iri,
    )
    location = first(descriptions, None)

    if not location:
        raise ValueError(f'Page not found by IRI: {iri}')

    return a(
        '📃 ',
        location['label'],
        href=location['url'],
    )
