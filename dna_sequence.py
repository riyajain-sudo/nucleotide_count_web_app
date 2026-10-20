"""Parsing and counting for raw DNA or a single-record FASTA input."""
from collections import Counter
import re

# IUPAC DNA symbols; ambiguous symbols are retained as an explicit category.
DNA_SYMBOLS = set("ACGTRYSWKMBDHVN")
AMBIGUOUS_SYMBOLS = DNA_SYMBOLS - set("ACGT")
MAX_SEQUENCE_LENGTH = 1_000_000

def parse_sequence(text: str, max_length: int = MAX_SEQUENCE_LENGTH) -> str:
    """Return normalized DNA, accepting raw text or exactly one FASTA record.

    Whitespace is formatting and removed. RNA U, gaps, punctuation, and other
    non-IUPAC symbols are rejected rather than silently omitted.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be text.")
    lines = text.splitlines()
    first = next((line.strip() for line in lines if line.strip()), "")
    if not first:
        raise ValueError("Enter a DNA sequence; input is empty.")
    if first.startswith(">"):
        records = []
        current = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current is not None:
                    records.append(current)
                current = []
            else:
                if current is None:
                    raise ValueError("FASTA sequence data must follow its header.")
                current.append(line)
        if current is not None:
            records.append(current)
        if len(records) != 1:
            raise ValueError("Only a single FASTA record is supported.")
        sequence = "".join(records[0])
    else:
        if any(line.lstrip().startswith(">") for line in lines):
            raise ValueError("FASTA header must be the first non-empty line.")
        sequence = "".join(lines)
    sequence = re.sub(r"\s+", "", sequence).upper()
    if not sequence:
        raise ValueError("Input contains no sequence symbols.")
    if len(sequence) > max_length:
        raise ValueError(f"Sequence exceeds the {max_length:,}-symbol limit.")
    invalid = sorted(set(sequence) - DNA_SYMBOLS)
    if invalid:
        symbols = ", ".join(repr(symbol) for symbol in invalid)
        raise ValueError(f"Unsupported DNA symbol(s): {symbols}. RNA U and gaps are not accepted.")
    return sequence

def count_nucleotides(sequence: str) -> dict[str, int]:
    """Count A/C/G/T and combined IUPAC ambiguity without losing symbols."""
    counts = Counter(sequence)
    result = {base: counts[base] for base in "ATGC"}
    result["Ambiguous"] = sum(counts[base] for base in AMBIGUOUS_SYMBOLS)
    result["Total"] = len(sequence)
    assert sum(result[base] for base in ("A", "T", "G", "C", "Ambiguous")) == result["Total"]
    return result
