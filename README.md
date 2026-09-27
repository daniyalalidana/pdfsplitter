# PDF Page Splitter

A small Python utility for extracting an inclusive range of pages from a PDF into a new PDF. It provides a Streamlit web interface and a command-line interface.

## Requirements

- Python 3.9 or newer
- `uv` for the recommended launcher, or `pip`

## Installation

Using `uv`:

```bash
uv sync
```

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Web interface

Start the Streamlit application with:

```bash
./run_pdf_splitter.sh
```

The launcher starts the app at <http://localhost:8501> and attempts to open it in your browser. Upload a PDF, choose the start and end pages, enter an output filename, and select **Split PDF**.

You can also start it manually:

```bash
streamlit run app.py
```

If you use the desktop shortcut, open `PDF Splitter.desktop`. Its `Exec` and `Path` entries contain the current absolute project path, so update them if the project is moved.

## Command line

Extract pages 1 through 10:

```bash
python app.py input.pdf --start 1 --end 10 --output selected-pages.pdf
```

Arguments:

- `input_pdf`: path to the source PDF
- `--start`: first page to extract, using 1-based numbering
- `--end`: last page to extract, using 1-based numbering
- `-o`, `--output`: output path; if omitted, a name is generated from the input filename

For example:

```bash
python app.py document.pdf --start 5 --end 12
```

This creates `document_pages_5_12.pdf` beside the source file.

## License

No license has been specified for this project.
