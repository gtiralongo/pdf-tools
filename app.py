import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        reader = PdfReader(pdf)
        merger.append(reader)
    merged_pdf_path = "merged.pdf"
    with open(merged_pdf_path, "wb") as f:
        merger.write(f)
    return merged_pdf_path

def compress_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    for i in range(len(reader.pages)):
        writer.add_page(reader.pages[i])
    
    compressed_pdf_path = "compressed.pdf"
    with open(compressed_pdf_path, "wb") as f:
        writer.write(f)
    return compressed_pdf_path

def main():
    st.title("Herramienta para unir y comprimir PDFs")
    
    st.header("Unir PDFs")
    uploaded_files = st.file_uploader("Sube tus PDFs", type=["pdf"], accept_multiple_files=True)
    if st.button("Unir PDFs"):
        if uploaded_files:
            merged_pdf = merge_pdfs(uploaded_files)
            st.success("PDFs unidos correctamente!")
            with open(merged_pdf, "rb") as f:
                st.download_button(label="Descargar PDF unido", data=f, file_name="merged.pdf", mime="application/pdf")
        else:
            st.error("Sube al menos un archivo PDF.")
    
    st.header("Comprimir PDF")
    uploaded_file = st.file_uploader("Sube tu PDF para comprimir", type=["pdf"], key="compress")
    if st.button("Comprimir PDF"):
        if uploaded_file:
            compressed_pdf = compress_pdf(uploaded_file)
            st.success("PDF comprimido correctamente!")
            with open(compressed_pdf, "rb") as f:
                st.download_button(label="Descargar PDF comprimido", data=f, file_name="compressed.pdf", mime="application/pdf")
        else:
            st.error("Sube un archivo PDF.")
    
if __name__ == "__main__":
    main()
