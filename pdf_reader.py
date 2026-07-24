"""
============================================================
EduMindAI Enterprise v3.0
PDF Reader
============================================================
"""

import os
import fitz  # PyMuPDF


class PDFReader:

    def __init__(self):

        pass

    # =====================================================
    # READ PDF
    # =====================================================

    def read_pdf(
        self,
        file
    ):

        try:

            document = fitz.open(stream=file.read(), filetype="pdf")

            text = ""

            for page in document:

                text += page.get_text()

            document.close()

            return text

        except Exception:

            return ""

    # =====================================================
    # READ TXT
    # =====================================================

    def read_txt(
        self,
        file
    ):

        try:

            return file.read().decode("utf-8")

        except Exception:

            return ""
            # =====================================================
    # READ MULTIPLE FILES
    # =====================================================

    def read_multiple(
        self,
        files
    ):

        text = ""

        for file in files:

            extension = file.name.split(".")[-1].lower()

            if extension == "pdf":

                text += self.read_pdf(file)

            elif extension == "txt":

                text += self.read_txt(file)

            text += "\n\n"

        return text

    # =====================================================
    # FILE TYPE
    # =====================================================

    def file_type(
        self,
        file
    ):

        return file.name.split(".")[-1].lower()
        # =====================================================
    # FILE COUNT
    # =====================================================

    def count_pages(
        self,
        file
    ):

        try:

            document = fitz.open(
                stream=file.read(),
                filetype="pdf"
            )

            pages = len(document)

            document.close()

            return pages

        except Exception:

            return 0

    # =====================================================
    # CHECK
    # =====================================================

    def is_supported(
        self,
        filename
    ):

        extension = filename.split(".")[-1].lower()

        return extension in [

            "pdf",

            "txt"

        ]


# =====================================================
# PDF OBJECT
# =====================================================

pdf_reader = PDFReader()

