import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
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

def compress_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    for i in range(len(reader.pages)):
        writer.add_page(reader.pages[i])
    
    compressed_pdf_path = "compressed.pdf"
    with open(compressed_pdf_path, "wb") as f:
        writer.write(f)
    return compressed_pdf_path

def split_pdf(input_pdf_path, output_folder, pages_per_file):
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for start_page in range(0, total_pages, pages_per_file):
        writer = PdfWriter()
        end_page = min(start_page + pages_per_file, total_pages)
        for i in range(start_page, end_page):
            writer.add_page(reader.pages[i])
        
        output_pdf_path = os.path.join(output_folder, f"split_{start_page + 1}_to_{end_page}.pdf")
        with open(output_pdf_path, "wb") as f:
            writer.write(f)
    
    return output_folder

def main():
    st.title("Herramienta para unir, comprimir y dividir PDFs")

    tab1, tab2, tab3 = st.tabs(["Unir PDFs", "Comprimir PDF", "Dividir PDF"])

    with tab1:
        st.header("Unir PDFs")
        uploaded_files = st.file_uploader("Sube tus PDFs", type=["pdf"], accept_multiple_files=True, key="merge")
        if st.button("Unir PDFs"):
            if uploaded_files:
                merged_pdf = merge_pdfs(uploaded_files)
                st.success("PDFs unidos correctamente!")
                with open(merged_pdf, "rb") as f:
                    st.download_button(label="Descargar PDF unido", data=f, file_name="merged.pdf", mime="application/pdf")
            else:
                st.error("Sube al menos un archivo PDF.")

    with tab2:
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

    with tab3:
        st.header("Dividir PDF")
        uploaded_file = st.file_uploader("Sube tu PDF para dividir", type=["pdf"], key="split")
        pages_per_file = st.number_input("Páginas por archivo dividido", min_value=1, max_value=1000, value=2)
        if st.button("Dividir PDF"):
            if uploaded_file:
                with open("temp_uploaded.pdf", "wb") as f:
                    f.write(uploaded_file.read())

                output_folder = "split_pdfs"
                split_pdf("temp_uploaded.pdf", output_folder, pages_per_file)

                st.success("PDF dividido correctamente! Archivos divididos en la carpeta 'split_pdfs'.")
                os.remove("temp_uploaded.pdf")  # Limpiar el archivo temporal

                for split_file in os.listdir(output_folder):
                    with open(os.path.join(output_folder, split_file), "rb") as f:
                        st.download_button(label=f"Descargar {split_file}", data=f, file_name=split_file, mime="application/pdf")
            else:
                st.error("Sube un archivo PDF.")

if __name__ == "__main__":
    main()
