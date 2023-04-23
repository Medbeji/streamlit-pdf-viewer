import fitz
import io
from PIL import Image
import base64

def pdf_to_images_with_highlights(pdf_data, keyword):
    pdf = fitz.open(stream=pdf_data, filetype="pdf")
    images = []
    matching_pages = []

    for page_number in range(len(pdf)):
        page = pdf[page_number]
        matching_areas = []

        for match in page.search_for(keyword):
            matching_areas.append(match)

        if matching_areas:
            matching_pages.append(page_number + 1)

        for area in matching_areas:
            page.add_highlight_annot(area)

        dl = page.get_displaylist()
        highlighted_page = dl.get_pixmap()

        img = Image.frombytes("RGB", (highlighted_page.width, highlighted_page.height), highlighted_page.samples)
        images.append(img)

    return images, matching_pages

def get_image_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str
