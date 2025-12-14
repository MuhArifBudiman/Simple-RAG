from pypdf import PdfReader
import os

THIS_PATH = os.getcwd()
PDF_DIR = os.path.join(THIS_PATH, "source", "CV_Muhammad Arif Budiman.pdf")


def clean_text(text: str):
    if not text:
        return ""
    text = text.strip()
    return text


def reader(pdf_path: str):

    if pdf_path.endswith('.pdf'):
        result_pdf = PdfReader(pdf_path)
    else:
        raise "Please upload pdf"

    if len(result_pdf.pages) == 1:
        text = result_pdf.pages[0].extract_text()
        result_text = clean_text(text=text)
        return result_text
    else:
        all_text = []
        for page in result_pdf.pages:
            t = page.extract_text()
            if t:
                all_text.append(t)
        result_text = clean_text("\n".join(all_text))

        return result_text


if __name__ == '__main__':
    result = reader(pdf_path=PDF_DIR)
    print(result)
