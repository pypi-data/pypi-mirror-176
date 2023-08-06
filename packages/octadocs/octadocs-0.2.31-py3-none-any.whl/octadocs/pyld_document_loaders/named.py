from dataclasses import dataclass
from typing import Any, Dict

from octadocs.pyld_document_loaders.base import DocumentLoader
from octadocs.pyld_document_loaders.models import JsonLDDocument
from pyld.jsonld import JsonLdError
from urlpath import URL


@dataclass
class NamedLoader(DocumentLoader):
    """
    Load JSON document from a named:// IRI.

    The mappings have been configured in mkdocs.yml, at extra.named section.
    """

    documents: Dict[str, Any]

    def __call__(self, url: str, options: Dict[str, Any]) -> JsonLDDocument:
        decoded_url = URL(url)

        if decoded_url.scheme == 'local':
            document_name = decoded_url.path

        else:
            raise ValueError('Scheme must be `local`.')

        try:
            response = {
                'document': self.documents[document_name],
                'contextUrl': None,
                'documentUrl': url,
                'contentType': 'application/ld+json',
            }
        except KeyError:
            raise JsonLdError(
                message=(
                    f'Cannot find a document under `{document_name}` label. '
                    f'Please check your mkdocs.yml configuration '
                    f'or plugin code.'
                ),
                type_='jsonld.InvalidUrl',
                details={
                    'url': url,
                    'named_contexts': list(self.documents.keys()),
                },
                code='loading document failed',
            )

        return response
