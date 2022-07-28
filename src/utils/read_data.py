import pdfplumber
import pdf2image

def pdf_to_text(path: str):
    all_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            all_text += '\n' + text

    return all_text


def pdf_to_image(path: str):
    pages = pdf2image.convert_from_path(
        pdf_path=path, dpi=200, size=(1654,2340))

    return pages
