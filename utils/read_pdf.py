from pypdf import PdfReader
import os

THIS_PATH = os.getcwd()
PDF_DIR = os.path.join(THIS_PATH,"source","CV_Muhammad Arif Budiman.pdf")


reader = PdfReader(PDF_DIR)

print(PDF_DIR)
print(reader.pages[1].extract_text())

def clean_text(text:str):
    text = text.replace("\n", " ")
    text = " ".join(text.split())  # remove extra spaces
    return text

def reader(pdf_path:str):
    
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
        
        return clean_text("\n".join(all_text))
