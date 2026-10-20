# DNA Nucleotide Count Web App

Streamlit demo for a **raw DNA sequence** or **one-record FASTA**. Input is normalized to uppercase; line wrapping and whitespace are ignored. DNA IUPAC ambiguity symbols `RYSWKMBDHVN` are accepted and reported together as **Ambiguous**, while A/C/G/T are counted separately. RNA `U`, gaps, punctuation, empty input, and multiple FASTA records are rejected explicitly. Maximum normalized length: 1,000,000 symbols.

## Run locally

Python 3.10+ is recommended. From this directory:

```sh
python -m venv .venv
. .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The logo is resolved relative to `app.py`; launch from another working directory with `streamlit run /path/to/nucleotide_count_web_app/app.py`. Example: `>sample\nacgtNN` produces A=1, C=1, G=1, T=1, ambiguous=2, total=6.

Run parser regression tests (no Streamlit installation required): `python -m unittest discover -s tests -v`. Counts are composition only; ambiguous bases are not identified individually in the chart.
