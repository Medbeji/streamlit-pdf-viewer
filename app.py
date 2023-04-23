import streamlit as st
from pdf_processing import pdf_to_images_with_highlights, get_image_base64

def main():
    st.set_page_config(page_title="DocGPT", layout="wide")
    st.title("DocGPT")
    setup_style()

    col1, col_separator, col2 = st.columns([1, 0.4, 2])
    col_separator.markdown('<div class="line-separator"></div>', unsafe_allow_html=True)

    uploaded_pdf, keyword_input, search_button = input_section(col1)
    search_clicked = st.session_state.get("search_clicked", False)
     
    if (uploaded_pdf and keyword_input and search_button) or (uploaded_pdf and keyword_input and search_clicked):
        if search_button:
            st.session_state.search_clicked = True
        pdf_data = uploaded_pdf.read()

        
        images, matching_pages = pdf_to_images_with_highlights(pdf_data, keyword_input)
        images_base64 = [get_image_base64(image) for image in images]

        if search_button and matching_pages:
            st.session_state.page_number = matching_pages[0]
            st.session_state.matching_pages = matching_pages

        results_section(col1, matching_pages, search_clicked, search_button)
        preview_section(col2, images)
    else: 
        st.write("Please make sure you upload a file and input a keyword to search for !")

def setup_style():
    st.markdown("""
    <style>
        .line-separator {
            border-left: 1px solid #000;
            height: 100%;
            margin: 0 16px;
            color: grey;
        }
    </style>
    """, unsafe_allow_html=True)

def input_section(column):
    with column:
        st.header("PDF Keyword Search")
        uploaded_pdf = st.file_uploader("Upload a PDF document", type=["pdf"])
        keyword_input = st.text_input("Enter keywords to search in the PDF")
        search_button = st.button("Search")
    return uploaded_pdf, keyword_input, search_button

def results_section(column, matching_pages, search_clicked, search_button):
    with column:
        if (search_clicked and 'matching_pages' in st.session_state) or search_button:
            if not 'matching_pages' in st.session_state or len(st.session_state.matching_pages) == 0: 
                st.markdown("No results found!")
            else: 
                st.markdown("Found results in the following pages:")
                columns = st.columns(len(st.session_state.matching_pages))
                for idx, p in enumerate(matching_pages):
                    with columns[idx]: 
                        if st.button(f"{p}"):
                            st.session_state.page_number = p
                            st.session_state.search_clicked = True

def preview_section(column, images):
    with column:
        st.header("PDF Preview with Highlighted Keywords")
        with st.spinner('Loading document'):
            total_pages = len(images)
            page_number = st.session_state.get('page_number', 1)
            col1, col2, col3 = st.columns(3)
            if col1.button('Previous', key='previous_top'):
                page_number = max(page_number - 1, 1)
                st.session_state.page_number = page_number
            col2.write(f"Page {page_number} of {total_pages}")
            if col3.button('Next', key='next_top'):
                page_number = min(page_number + 1, total_pages)
                st.session_state.page_number = page_number

            st.image(images[page_number - 1], width=None, use_column_width="auto")

if __name__ == "__main__":
    main()