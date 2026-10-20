from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
from PIL import Image

from dna_sequence import count_nucleotides, parse_sequence

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="DNA Nucleotide Count", page_icon="🧬")
st.image(Image.open(ROOT / "dna-logo.jpg"), use_container_width=True)
st.title("DNA Nucleotide Count Web App")
st.write("Count A/C/G/T and IUPAC ambiguity symbols in raw DNA or a single-record FASTA.")
example = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAG\nGACGGAAGGTCCTGTGCTCGGG"
raw = st.text_area("Sequence input", example, height=250)
try:
    sequence = parse_sequence(raw)
except ValueError as error:
    st.info(str(error))
else:
    counts = count_nucleotides(sequence)
    st.subheader("Normalized input")
    st.code(sequence, language=None)
    st.subheader("Composition")
    st.write(counts)
    st.caption(f"Total symbols: {counts['Total']:,}; ambiguous IUPAC symbols: {counts['Ambiguous']:,}.")
    chart_data = pd.DataFrame(
        [(base, counts[base]) for base in ("A", "T", "G", "C", "Ambiguous")],
        columns=["category", "count"],
    )
    st.dataframe(chart_data, hide_index=True)
    st.altair_chart(alt.Chart(chart_data).mark_bar().encode(x="category:N", y="count:Q"), use_container_width=True)
