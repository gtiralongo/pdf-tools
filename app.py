import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import ghostscript
import os

def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        reader = PdfReader(pdf)
        merger.append(reader)
    merged_pdf_path = "merged.pdf"
    with open(merged_pdf_path, "wb") as f:
        merger.write(f)
    return merged_pdf_path

def compress_pdf(input_pdf_path, output_pdf_path):
    args = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/screen",  # Cambia a /ebook, /printer o /prepress para diferentes niveles de compresión
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-dColorImageDownsampleType=/Bicubic",
        "-dColorImageResolution=72",
        "-dGrayImageDownsampleType=/Bicubic",
        "-dGrayImageResolution=72",
        "-dMonoImageDownsampleType=/Subsample",
        "-dMonoImageResolution=72",
        f"-sOutputFile={output_pdf_path}",
        input_pdf_path,
    ]

    ghostscript.Ghostscript(*args)
    return output_pdf_path

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
            with open("temp_uploaded.pdf", "wb") as f:
                f.write(uploaded_file.read())
            compressed_pdf = compress_pdf("temp_uploaded.pdf", "compressed.pdf")
            st.success("PDF comprimido correctamente!")
            with open(compressed_pdf, "rb") as f:
                st.download_button(label="Descargar PDF comprimido", data=f, file_name="compressed.pdf", mime="application/pdf")
            os.remove("temp_uploaded.pdf")  # Limpiar el archivo temporal
        else:
            st.error("Sube un archivo PDF.")
    
if __name__ == "__main__":
    main()
