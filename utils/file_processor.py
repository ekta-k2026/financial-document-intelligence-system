
import pandas as pd
from pypdf import PdfReader
from io import BytesIO
import streamlit as st

from fintech.kpi_extractor import extract_kpis
from fintech.categorizer import detect_category

from ocr.ocr_processor import (
    extract_text_from_scanned_pdf
)
def process_uploaded_file(file_bytes, file_name):

    df = None
    kpis = {}


    documents = []
    full_text = ""
    df = None
    kpis = {}

    # -------- TXT --------
    if file_name.endswith(".txt"):

        content = file_bytes.decode("utf-8")

        full_text = content

        sentences = content.split(".")

        for i in range(0, len(sentences), 2):

            chunk = ".".join(
                sentences[i:i+2]
            )

            if chunk.strip():

                documents.append(
                    f"[{file_name}] {chunk}"
                )

    # -------- PDF --------
    elif file_name.endswith(".pdf"):

        file = BytesIO(file_bytes)

        reader = PdfReader(file)

        content = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:

                content += text + " "

        # -------- OCR FALLBACK --------
        if content.strip() == "":

            content = extract_text_from_scanned_pdf(
                file_bytes
            )

        full_text = content

        sentences = content.split(".")

        for i in range(0, len(sentences), 2):

            chunk = ".".join(
                sentences[i:i+2]
            )

            if chunk.strip():

                documents.append(
                    f"[{file_name}] {chunk}"
                )

    # -------- EXCEL --------
    elif file_name.endswith(".xlsx"):

        file = BytesIO(file_bytes)

        dfs = pd.read_excel(
            file,
            sheet_name=None
        )

        sheet_names = list(dfs.keys())

        key = f"sheets_{file_name}"

        if key not in st.session_state:

            st.session_state[key] = sheet_names

        selected_sheets = st.multiselect(
            f"Select sheets for {file_name}",
            sheet_names,
            default=st.session_state[key],
            key=key
        )

        for sheet in selected_sheets:

            df = dfs[sheet].fillna("")

            # -------- AUTO CATEGORY --------
            if "Description" in df.columns:

                df["AI_Category"] = df[
                    "Description"
                ].apply(detect_category)

            # -------- PREVIEW --------
            st.subheader(f"📊 Preview: {sheet}")

            st.dataframe(df.head())

            # -------- KPI EXTRACTION --------
            kpis = extract_kpis(df)

            st.subheader("📈 Financial KPIs")

            for key, value in kpis.items():

                st.write(f"**{key}:** {value}")

            # -------- DOCUMENT CREATION --------
            for _, row in df.iterrows():

                row_text = " | ".join(
                    [str(x) for x in row.values]
                )

                if row_text.strip():

                    documents.append(
                        f"[{file_name} | {sheet}] {row_text}"
                    )

            # -------- NUMERIC SUMMARY --------
            numeric_cols = df.select_dtypes(
                include=["number"]
            )

            if not numeric_cols.empty:

                summary = numeric_cols.describe().to_string()

                documents.append(
                    f"[{file_name} | {sheet}] NUMERIC SUMMARY: {summary}"
                )

            full_text += df.to_string()

    # -------- UNKNOWN FILE --------
    else:

        return [], "", None, {}

    return documents, full_text, df, kpis


