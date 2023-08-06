"""Top-level package for alignme."""

__author__ = "xichenwu"
__email__ = "xichenwu@outlook.com"
__version__ = "0.1.0"


from Bio import pairwise2
from Bio.Seq import Seq


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
