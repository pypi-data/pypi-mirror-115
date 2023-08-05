# -*- coding: utf-8 -*-

"""Selventa complexes."""

from typing import Iterable, Optional

import pandas as pd

from pyobo import Obo, Term
from pyobo.utils.path import ensure_df

PREFIX = "scomp"
URL = "https://raw.githubusercontent.com/OpenBEL/resource-generator/master/datasets/selventa-named-complexes.txt"


def get_obo(*, force: bool = False) -> Obo:
    """Get Selventa Complexes as OBO."""
    return Obo(
        ontology=PREFIX,
        name="Selventa Complexes",
        iter_terms=iter_terms,
        iter_terms_kwargs=dict(force=force),
        data_version="1.0.0",
        auto_generated_by=f"bio2obo:{PREFIX}",
    )


def iter_terms(force: Optional[bool] = False) -> Iterable[Term]:
    """Iterate over selventa complex terms."""
    df = ensure_df(PREFIX, url=URL, skiprows=9, force=force)

    terms = {}
    for identifier, label, synonyms, xref in df[["ID", "LABEL", "SYNONYMS", "XREF"]].values:
        term = Term.from_triple(PREFIX, identifier, label)
        for synonym in synonyms.split("|") if pd.notna(synonyms) else []:
            term.append_synonym(synonym)
        if pd.notna(xref):
            term.append_xref(xref)
        terms[identifier] = term

    df.PARENTS = df.PARENTS.map(lambda x: x[len("SCOMP:") :], na_action="ignore")
    for child, parent in df.loc[df.PARENTS.notna(), ["ID", "PARENTS"]].values:
        if child == parent:
            continue  # wow...
        terms[child].append_parent(terms[parent])

    yield from terms.values()


if __name__ == "__main__":
    get_obo().write_default(write_obo=True, force=True)
