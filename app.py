import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os
from pdf2image import convert_from_path
from PIL import Image

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

def split_pdf(input_pdf_path, pages_per_file):
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    split_files = []
    for start_page in range(0, total_pages, pages_per_file):
        writer = PdfWriter()
        end_page = min(start_page + pages_per_file, total_pages)
        for i in range(start_page, end_page):
            writer.add_page(reader.pages[i])
        
        output_pdf_path = f"split_{start_page + 1}_to_{end_page}.pdf"
        with open(output_pdf_path, "wb") as f:
            writer.write(f)
        
        split_files.append(output_pdf_path)
    
    return split_files

def pdf_to_images(pdf_file):
    images = convert_from_path(pdf_file)
    image_paths = []
    for i, image in enumerate(images):
        image_path = f"page_{i + 1}.png"
        image.save(image_path, "PNG")
        image_paths.append(image_path)
    return image_paths

def images_to_pdf(image_files):
    images = [Image.open(img).convert("RGB") for img in image_files]
    pdf_path = "images_to_pdf.pdf"
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    return pdf_path

def main():
    st.title("Herramienta para unir, comprimir, dividir y convertir PDFs e imágenes")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Unir PDFs", "Comprimir PDF", "Dividir PDF", "PDF a Imágenes", "Imágenes a PDF"])

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

                split_files = split_pdf("temp_uploaded.pdf", pages_per_file)

                st.success("PDF dividido correctamente! Descarga los archivos divididos a continuación.")
                os.remove("temp_uploaded.pdf")  # Limpiar el archivo temporal

                for split_file in split_files:
                    with open(split_file, "rb") as f:
                        st.download_button(label=f"Descargar {split_file}", data=f, file_name=split_file, mime="application/pdf")
            else:
                st.error("Sube un archivo PDF.")

    with tab4:
        st.header("Convertir PDF a Imágenes")
        uploaded_file = st.file_uploader("Sube tu PDF para convertir a imágenes", type=["pdf"], key="pdf_to_images")
        if st.button("Convertir a Imágenes"):
            if uploaded_file:
                with open("temp_pdf.pdf", "wb") as f:
                    f.write(uploaded_file.read())
                image_files = pdf_to_images("temp_pdf.pdf")
                os.remove("temp_pdf.pdf")

                st.success("PDF convertido a imágenes!")
                for image_file in image_files:
                    with open(image_file, "rb") as img:
                        st.download_button(label=f"Descargar {image_file}", data=img, file_name=image_file, mime="image/png")
            else:
                st.error("Sube un archivo PDF.")

    with tab5:
        st.header("Convertir Imágenes a PDF")
        uploaded_images = st.file_uploader("Sube tus imágenes para convertir a PDF", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="images_to_pdf")
        if st.button("Convertir a PDF"):
            if uploaded_images:
                image_paths = []
                for uploaded_image in uploaded_images:
                    with open(uploaded_image.name, "wb") as f:
                        f.write(uploaded_image.read())
                        image_paths.append(uploaded_image.name)

                pdf_file = images_to_pdf(image_paths)

                st.success("Imágenes convertidas a PDF!")
                with open(pdf_file, "rb") as f:
                    st.download_button(label="Descargar PDF", data=f, file_name="images_to_pdf.pdf", mime="application/pdf")
                
                for img in image_paths:
                    os.remove(img)  # Eliminar las imágenes temporales
            else:
                st.error("Sube al menos una imagen.")

if __name__ == "__main__":
    main()
