# -*- coding: utf-8 -*-

"""Converter for FamPlex."""

import logging
from collections import defaultdict
from typing import Iterable, List, Mapping

import click
from more_click import verbose_option
from pystow.utils import get_commit

from pyobo import get_name_id_mapping
from pyobo.identifier_utils import normalize_prefix
from pyobo.struct import Obo, Reference, Term
from pyobo.struct.typedef import has_member, has_part, is_a, part_of
from pyobo.utils.io import multidict
from pyobo.utils.path import ensure_df

logger = logging.getLogger(__name__)

PREFIX = "fplx"


def get_obo(force: bool = False) -> Obo:
    """Get FamPlex as OBO."""
    version = get_commit("sorgerlab", "famplex")
    return Obo(
        ontology=PREFIX,
        name="FamPlex",
        iter_terms=get_terms,
        iter_terms_kwargs=dict(version=version, force=force),
        data_version=version,
        typedefs=[has_member, has_part, is_a, part_of],
        auto_generated_by=f"bio2obo:{PREFIX}",
    )


def get_terms(version: str, force: bool = False) -> Iterable[Term]:
    """Get the FamPlex terms."""
    base_url = f"https://raw.githubusercontent.com/sorgerlab/famplex/{version}"

    entities_url = f"{base_url}/entities.csv"
    entities_df = ensure_df(PREFIX, url=entities_url, version=version, dtype=str, force=force)

    relations_url = f"{base_url}/relations.csv"
    relations_df = ensure_df(
        PREFIX, url=relations_url, version=version, header=None, sep=",", dtype=str, force=force
    )

    definitions_url = f"{base_url}/descriptions.csv"
    definitions_df = ensure_df(
        PREFIX,
        url=definitions_url,
        version=version,
        header=None,
        sep=",",
        dtype=str,
        force=force,
    )
    id_to_definition = {
        identifier: (definition, provenance)
        for identifier, provenance, definition in definitions_df.values
    }

    id_xrefs = _get_xref_df(version)

    hgnc_name_to_id = get_name_id_mapping("hgnc")
    in_edges = defaultdict(list)
    out_edges = defaultdict(list)
    for h_ns, h_name, r, t_ns, t_name in relations_df.values:
        if h_ns == "HGNC":
            h_identifier = hgnc_name_to_id.get(h_name)
            if h_identifier is None:
                logger.warning(
                    "[%s] could not look up HGNC identifier for gene: %s", PREFIX, h_name
                )
            h = Reference(prefix="hgnc", identifier=h_identifier, name=h_name)
        elif h_ns == "FPLX":
            h = Reference(prefix="fplx", identifier=h_name, name=h_name)
        elif h_ns == "UP":
            continue
        else:
            logger.exception(h_ns)
            raise
        if t_ns == "HGNC":
            t_identifier = hgnc_name_to_id.get(t_name)
            if t_identifier is None:
                logger.warning(
                    "[%s] could not look up HGNC identifier for gene: %s", PREFIX, t_name
                )
            t = Reference(prefix="hgnc", identifier=t_identifier, name=t_name)
        elif t_ns == "FPLX":
            t = Reference(prefix="fplx", identifier=t_name, name=t_name)
        elif h_ns == "UP":
            continue
        else:
            raise

        out_edges[h].append((r, t))
        in_edges[t].append((r, h))

    for (entity,) in entities_df.values:
        reference = Reference(prefix=PREFIX, identifier=entity, name=entity)
        definition, provenance = id_to_definition.get(entity, (None, None))
        term = Term(
            reference=reference,
            definition=definition,
            provenance=[Reference.from_curie(provenance)] if definition is not None else None,
        )

        for xref_reference in id_xrefs.get(entity, []):
            term.append_xref(xref_reference)

        for r, t in out_edges.get(reference, []):
            if r == "isa" and t.prefix == "fplx":
                term.append_parent(t)
            elif r == "isa":
                term.append_relationship(is_a, t)
            elif r == "partof":
                term.append_relationship(part_of, t)
            else:
                logging.warning("unhandled relation %s", r)

        for r, h in in_edges.get(reference, []):
            if r == "isa":
                term.append_relationship(has_member, h)
            elif r == "partof":
                term.append_relationship(has_part, h)
            else:
                logging.warning("unhandled relation %s", r)
        yield term


def _get_xref_df(version: str) -> Mapping[str, List[Reference]]:
    base_url = f"https://raw.githubusercontent.com/sorgerlab/famplex/{version}"
    xrefs_url = f"{base_url}/equivalences.csv"
    xrefs_df = ensure_df(PREFIX, url=xrefs_url, version=version, header=None, sep=",", dtype=str)

    # Normalize nextprot families
    ns_remapping = {
        "NXP": "nextprot.family",
    }
    xrefs_df[0] = xrefs_df[0].map(lambda s: ns_remapping.get(s, s))
    xrefs_df[1] = [
        xref_identifier if xref_prefix != "nextprot.family" else xref_identifier[len("FA:") :]
        for xref_prefix, xref_identifier in xrefs_df[[0, 1]].values
    ]

    xrefs_df[0] = xrefs_df[0].map(normalize_prefix)
    xrefs_df = xrefs_df[xrefs_df[0].notna()]
    xrefs_df = xrefs_df[xrefs_df[0] != "bel"]
    return multidict(
        (identifier, Reference(xref_prefix, xref_identifier))
        for xref_prefix, xref_identifier, identifier in xrefs_df.values
    )


@click.command()
@verbose_option
def _main():
    get_obo(force=True).write_default(use_tqdm=True, write_obo=True)


if __name__ == "__main__":
    _main()
