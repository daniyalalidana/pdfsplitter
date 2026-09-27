#!/usr/bin/env python3

from __future__ import annotations

import argparse
import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter


START_PAGE = 980
END_PAGE = 990


def extract_pages(input_path: Path, output_path: Path, start_page: int, end_page: int) -> None:
    reader = PdfReader(str(input_path))
    writer = extract_pages_from_reader(reader, start_page, end_page)

    with output_path.open("wb") as output_file:
        writer.write(output_file)


def extract_pages_from_reader(reader: PdfReader, start_page: int, end_page: int) -> PdfWriter:
    total_pages = len(reader.pages)

    if start_page < 1 or end_page < start_page:
        raise ValueError("Invalid page range")
    if end_page > total_pages:
        raise ValueError(f"PDF has only {total_pages} pages, but requested up to page {end_page}")

    writer = PdfWriter()
    for page_number in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_number])

    return writer


def build_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_pages_{START_PAGE}_{END_PAGE}.pdf")


def run_streamlit_app() -> None:
    import streamlit as st

    st.set_page_config(page_title="PDF Page Splitter", page_icon=":page_facing_up:", layout="centered")
    st.title("PDF Page Splitter")

    uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_pdf is None:
        st.info("Upload a PDF, then enter the page numbers you want to extract.")
        return

    try:
        reader = PdfReader(uploaded_pdf)
        total_pages = len(reader.pages)
    except Exception as error:
        st.error(f"Could not read this PDF: {error}")
        return

    st.caption(f"Total pages: {total_pages}")

    col1, col2 = st.columns(2)
    with col1:
        start_page = st.number_input(
            "Start page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
        )
    with col2:
        end_page = st.number_input(
            "End page",
            min_value=1,
            max_value=total_pages,
            value=total_pages,
            step=1,
        )

    output_name = st.text_input(
        "Output file name",
        value=f"{Path(uploaded_pdf.name).stem}_pages_{start_page}_{end_page}.pdf",
    )

    if st.button("Split PDF", type="primary"):
        try:
            writer = extract_pages_from_reader(reader, int(start_page), int(end_page))
            output_buffer = io.BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)
        except Exception as error:
            st.error(f"Could not split PDF: {error}")
            return

        st.success(f"Ready: pages {start_page}-{end_page}")
        st.download_button(
            "Download split PDF",
            data=output_buffer,
            file_name=output_name if output_name.endswith(".pdf") else f"{output_name}.pdf",
            mime="application/pdf",
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"Extract pages {START_PAGE} to {END_PAGE} from a PDF into a new file."
    )
    parser.add_argument("input_pdf", type=Path, help="Path to the source PDF")
    parser.add_argument(
        "--start",
        type=int,
        default=START_PAGE,
        help=f"First page to extract (1-based). Defaults to {START_PAGE}",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=END_PAGE,
        help=f"Last page to extract (1-based). Defaults to {END_PAGE}",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output PDF path. Defaults to <input_stem>_pages_980_990.pdf",
    )
    args = parser.parse_args()

    input_path = args.input_pdf
    start_page = args.start
    end_page = args.end

    def build_output_path_for_range(input_path: Path, start: int, end: int) -> Path:
        return input_path.with_name(f"{input_path.stem}_pages_{start}_{end}.pdf")

    output_path = args.output if args.output else build_output_path_for_range(input_path, start_page, end_page)

    if not input_path.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_path}")

    extract_pages(input_path, output_path, start_page, end_page)
    print(f"Saved pages {start_page}-{end_page} to {output_path}")


if __name__ == "__main__":
    try:
        import streamlit.runtime.scriptrunner as streamlit_runner
    except ImportError:
        streamlit_runner = None

    if streamlit_runner and streamlit_runner.get_script_run_ctx():
        run_streamlit_app()
    else:
        main()
