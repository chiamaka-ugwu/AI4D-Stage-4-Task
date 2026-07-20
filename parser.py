from io import BytesIO
from fastapi import HTTPException
import PyPDF2
import docx


def extract_text(filename: str, content: bytes) -> str:
    """
    Extract text from supported document types.

    Supported formats:
    - .txt
    - .md
    - .pdf
    - .docx
    """

    filename = filename.lower()

    # TXT / Markdown
    if filename.endswith(".txt") or filename.endswith(".md"):
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1", errors="ignore")

    # PDF
    elif filename.endswith(".pdf"):

        try:
            reader = PyPDF2.PdfReader(BytesIO(content))

            pages = []

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    pages.append(text)

            return "\n".join(pages)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unable to read PDF: {str(e)}")

    # DOCX
    elif filename.endswith(".docx"):

        try:
            document = docx.Document(BytesIO(content))

            paragraphs = [paragraph.text for paragraph in document.paragraphs]

            return "\n".join(paragraphs)

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Unable to read DOCX: {str(e)}"
            )

    # Unsupported File
    raise HTTPException(status_code=400, detail="Unsupported file type.")
