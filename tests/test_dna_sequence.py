import unittest
from dna_sequence import count_nucleotides, parse_sequence

class SequenceParserTests(unittest.TestCase):
    def test_raw_single_line_and_wrapped(self):
        self.assertEqual(parse_sequence("acgt"), "ACGT")
        self.assertEqual(parse_sequence("AC\nGT\tNN"), "ACGTNN")
    def test_one_fasta_record_and_preserves_first_base(self):
        self.assertEqual(parse_sequence(">query\nacg\ntt"), "ACGTT")
    def test_multiple_records_rejected(self):
        with self.assertRaisesRegex(ValueError, "single FASTA"):
            parse_sequence(">one\nAC\n>two\nGT")
    def test_ambiguity_and_total_accounting(self):
        self.assertEqual(count_nucleotides(parse_sequence("ACGTNNRY")),
                         {"A": 1, "T": 1, "G": 1, "C": 1, "Ambiguous": 4, "Total": 8})
    def test_empty_rna_and_punctuation_rejected(self):
        for text in ("", "  \n", "ACGU", "AC-G", "AC.G"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_sequence(text)

if __name__ == "__main__":
    unittest.main()
