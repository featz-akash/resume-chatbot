import fitz
import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'])

def read_pdf(uploaded_file):

    
    pdf_bytes = uploaded_file.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in doc:

        pix = page.get_pixmap(dpi=300)

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        result = reader.readtext(np.array(img), detail=0)

        text += " ".join(result)
        text += "\n"

    return text