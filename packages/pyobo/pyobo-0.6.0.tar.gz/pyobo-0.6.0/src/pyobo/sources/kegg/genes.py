# -*- coding: utf-8 -*-

"""Convert KEGG Genes to OBO.

Run with ``python -m pyobo.sources.kegg.genes``
"""

import logging
from typing import Iterable, Optional

import bioversions
import click
from more_click import verbose_option
from tqdm import tqdm

from .api import (
    KEGGGenome,
    KEGG_GENES_PREFIX,
    SKIP,
    ensure_conv_genome_ncbigene,
    ensure_conv_genome_uniprot,
    ensure_list_genome,
    from_kegg_species,
)
from .genome import iter_kegg_genomes
from ...struct import Obo, Reference, Term, from_species, has_gene_product
from ...utils.io import open_map_tsv

logger = logging.getLogger(__name__)


def get_obo() -> Obo:
    """Get KEGG Genes as OBO."""
    version = bioversions.get_version("kegg")
    return Obo(
        ontology=KEGG_GENES_PREFIX,
        iter_terms=iter_terms,
        iter_terms_kwargs=dict(version=version),
        typedefs=[from_species, from_kegg_species, has_gene_product],
        name="KEGG Genes",
        data_version=version,
        auto_generated_by=f"bio2obo:{KEGG_GENES_PREFIX}",
    )


def iter_terms(version: str) -> Iterable[Term]:
    """Iterate over terms for KEGG Genome."""
    for kegg_genome in iter_kegg_genomes(version=version, desc="KEGG Genes"):
        if kegg_genome.identifier in SKIP:
            continue
        try:
            list_genome_path = ensure_list_genome(kegg_genome.identifier, version=version)
            conv_uniprot_path = ensure_conv_genome_uniprot(kegg_genome.identifier, version=version)
            conv_ncbigene_path = ensure_conv_genome_ncbigene(
                kegg_genome.identifier, version=version
            )
        except (OSError, ValueError) as e:
            tqdm.write(f"[{KEGG_GENES_PREFIX}] {kegg_genome.identifier} failed: {e}")
            continue

        yield from _make_terms(
            kegg_genome,
            list_genome_path,
            conv_uniprot_path,
            conv_ncbigene_path,
        )


def _make_terms(
    kegg_genome: KEGGGenome,
    list_genome_path: str,
    conv_uniprot_path: Optional[str] = None,
    conv_ncbigene_path: Optional[str] = None,
) -> Iterable[Term]:
    uniprot_conv = _load_conv(conv_uniprot_path, "up:") if conv_uniprot_path else {}
    ncbigene_conv = _load_conv(conv_ncbigene_path, "ncbi-geneid:") if conv_ncbigene_path else {}

    with open(list_genome_path) as file:
        for line in file:
            try:
                identifier, extras = line.strip().split("\t")
            except ValueError:
                logger.warning(
                    "[%s] could not parse line in %s: %s", KEGG_GENES_PREFIX, list_genome_path, line
                )
                continue
            if ";" in line:
                *_extras, name = [part.strip() for part in extras.split(";")]
            else:
                name = extras

            term = Term.from_triple(
                prefix=KEGG_GENES_PREFIX,
                identifier=identifier,
                name=name,
            )

            uniprot_xref = uniprot_conv.get(identifier)
            if uniprot_xref is not None:
                term.append_relationship(has_gene_product, Reference("uniprot", uniprot_xref))

            ncbigene_xref = ncbigene_conv.get(identifier)
            if ncbigene_xref is not None:
                term.append_xref(Reference("ncbigene", ncbigene_xref))

            kegg_genome.annotate_term(term)
            yield term


def _load_conv(path, value_prefix):
    m = open_map_tsv(path)
    m = {k: v[len(value_prefix) :] for k, v in m.items()}
    return m


@click.command()
@verbose_option
def _main():
    get_obo().write_default()


if __name__ == "__main__":
    _main()
