#!/usr/bin/env python
"""Command-line interface."""
import click
from Bio import pairwise2
from Bio.Seq import Seq
from rich import traceback


@click.command()
@click.version_option(version="1.0.0", message=click.style("alignment_tool Version: 1.0.0"))
def main() -> None:
    """alignment_tool."""


def read_dna(dna_file):
    """This function reads dna seq in a file."""
    with open(dna_file) as f:
        lines = f.read().replace("\n", "")
        seq = Seq(lines)
        return seq


def align(seq1, seq2):
    """This function aligna two sequences."""
    alignments = pairwise2.align.globalxx(seq1, seq2)
    return alignments[0]


if __name__ == "__main__":
    traceback.install()
    main(prog_name="alignment_tool")  # pragma: no cover
