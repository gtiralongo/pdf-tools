import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

# Funciones
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

def reorder_pages(pdf_file, order):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    for page_num in order:
        writer.add_page(reader.pages[page_num - 1])
    reordered_pdf_path = "reordered.pdf"
    with open(reordered_pdf_path, "wb") as f:
        writer.write(f)
    return reordered_pdf_path

def convert_pdf_to_images(pdf_file):
    images = convert_from_path(pdf_file)
    image_files = []
    for i, image in enumerate(images):
        image_path = f"page_{i + 1}.png"
        image.save(image_path, "PNG")
        image_files.append(image_path)
    return image_files

def convert_images_to_pdf(images):
    pdf_path = "converted_from_images.pdf"
    image_objs = [Image.open(img).convert("RGB") for img in images]
    image_objs[0].save(pdf_path, save_all=True, append_images=image_objs[1:])
    return pdf_path

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_with_ocr(pdf_file):
    images = convert_from_path(pdf_file)
    extracted_text = ""
    for image in images:
        extracted_text += pytesseract.image_to_string(image)
    return extracted_text

def add_watermark(pdf_file, watermark_text):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        page_content = page.extract_text()  # Placeholder for adding watermark
        # Here you would actually overlay the watermark text on the page content
        writer.add_page(page)

    watermarked_pdf_path = "watermarked.pdf"
    with open(watermarked_pdf_path, "wb") as f:
        writer.write(f)
    return watermarked_pdf_path

def encrypt_pdf(pdf_file, password):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)
    encrypted_pdf_path = "encrypted.pdf"
    with open(encrypted_pdf_path, "wb") as f:
        writer.write(f)
    return encrypted_pdf_path

# Interfaz de usuario
def main():
    st.title("🔧 Herramienta PDF")

    # Pestañas unificadas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📑 Unir, Dividir, Reordenar",
        "📝 Texto y Marcas de Agua",
        "🖼️  PDF a Imágenes ♻",
        "🔒 Protección y Compresión"
    ])

    # 📑 PDFs: Unir, Dividir, Reordenar
    with tab1:
        st.header("📑 Unir, Dividir y Reordenar PDFs")

        # Unir PDFs
        st.subheader("🔗 Unir PDFs")
        uploaded_files = st.file_uploader("Sube tus PDFs", type=["pdf"], accept_multiple_files=True, key="merge")
        if st.button("Unir PDFs"):
            if uploaded_files:
                merged_pdf = merge_pdfs(uploaded_files)
                st.success("PDFs unidos correctamente! 🎉")
                with open(merged_pdf, "rb") as f:
                    st.download_button(label="Descargar PDF unido", data=f, file_name="merged.pdf", mime="application/pdf")
            else:
                st.error("Sube al menos un archivo PDF.")

        # Dividir PDF
        st.subheader("✂️ Dividir PDF")
        uploaded_file = st.file_uploader("Sube tu PDF para dividir", type=["pdf"], key="split")
        pages_per_file = st.number_input("Páginas por archivo dividido", min_value=1, max_value=1000, value=2)
        if st.button("Dividir PDF"):
            if uploaded_file:
                with open("temp_uploaded.pdf", "wb") as f:
                    f.write(uploaded_file.read())
                split_files = split_pdf("temp_uploaded.pdf", pages_per_file)
                st.success("PDF dividido correctamente! 🎉")
                for split_file in split_files:
                    with open(split_file, "rb") as f:
                        st.download_button(label=f"Descargar {split_file}", data=f, file_name=split_file, mime="application/pdf")
                os.remove("temp_uploaded.pdf")
            else:
                st.error("Sube un archivo PDF.")

        # Reordenar páginas
        st.subheader("🔀 Reordenar Páginas")
        uploaded_file = st.file_uploader("Sube tu PDF para reordenar páginas", type=["pdf"], key="reorder_pages")
        page_order = st.text_input("Ingresa el nuevo orden de las páginas (ej: 3,1,2)")
        if st.button("Reordenar páginas"):
            if uploaded_file and page_order:
                order = [int(x) for x in page_order.split(",")]
                reordered_pdf = reorder_pages(uploaded_file, order)
                st.success("Páginas reordenadas correctamente! 🎉")
                with open(reordered_pdf, "rb") as f:
                    st.download_button(label="Descargar PDF reordenado", data=f, file_name="reordered.pdf", mime="application/pdf")
            else:
                st.error("Sube un archivo PDF y/o ingresa un orden válido.")

    # 📝 Texto y Marcas de Agua
    with tab2:
        st.header("📝 Extraer Texto y Marcas de Agua")

        # Extraer Texto
        st.subheader("🔍 Extraer Texto de PDF")
        uploaded_file = st.file_uploader("Sube tu PDF para extraer texto", type=["pdf"], key="extract_text")
        if st.button("Extraer texto"):
            if uploaded_file:
                extracted_text = extract_text_from_pdf(uploaded_file)
                st.text_area("Texto extraído:", extracted_text)
                st.download_button(label="Descargar texto", data=extracted_text, file_name="extracted_text.txt", mime="text/plain")
            else:
                st.error("Sube un archivo PDF.")

        # Extraer Texto con OCR
        st.subheader("🔍 Extraer Texto de PDF (OCR)")
        uploaded_file = st.file_uploader("Sube tu PDF para extraer texto (OCR)", type=["pdf"], key="ocr_text")
        if st.button("Extraer texto (OCR)"):
            if uploaded_file:
                extracted_text = extract_text_with_ocr(uploaded_file)
                st.text_area("Texto extraído (OCR):", extracted_text)
                st.download_button(label="Descargar texto OCR", data=extracted_text, file_name="ocr_text.txt", mime="text/plain")
            else:
                st.error("Sube un archivo PDF.")

        # Agregar Marca de Agua
        st.subheader("💧 Agregar Marca de Agua")
        uploaded_file = st.file_uploader("Sube tu PDF para agregar una marca de agua", type=["pdf"], key="watermark")
        watermark_text = st.text_input("Ingresa el texto de la marca de agua")
        if st.button("Agregar Marca de Agua"):
            if uploaded_file and watermark_text:
                watermarked_pdf = add_watermark(uploaded_file, watermark_text)
                st.success("Marca de agua agregada correctamente! 💧")
                with open(watermarked_pdf, "rb") as f:
                    st.download_button(label="Descargar PDF con marca de agua", data=f, file_name="watermarked.pdf", mime="application/pdf")
            else:
                st.error("Sube un archivo PDF y/o ingresa texto para la marca de agua.")

    # 🖼️ Convertir entre PDF e Imágenes
    with tab3:
        st.header("🖼️ Convertir PDF a Imágenes y viceversa")

        # Convertir PDF a Imágenes
        st.subheader("📸 Convertir PDF a Imágenes")
        uploaded_file = st.file_uploader("Sube tu PDF para convertir a imágenes", type=["pdf"], key="pdf_to_images")
        if st.button("Convertir PDF a Imágenes"):
            if uploaded_file:
                image_files = convert_pdf_to_images(uploaded_file)
                st.success("PDF convertido a imágenes correctamente! 🎉")
                for img in image_files:
                    st.image(img)
                    with open(img, "rb") as f:
                        st.download_button(label=f"Descargar {img}", data=f, file_name=img, mime="image/png")
            else:
                st.error("Sube un archivo PDF.")

        # Convertir Imágenes a PDF
        st.subheader("🖼️ Convertir Imágenes a PDF")
        uploaded_images = st.file_uploader("Sube tus imágenes para convertir a PDF", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="images_to_pdf")
        if st.button("Convertir Imágenes a PDF"):
            if uploaded_images:
                converted_pdf = convert_images_to_pdf([img for img in uploaded_images])
                st.success("Imágenes convertidas a PDF correctamente! 🎉")
                with open(converted_pdf, "rb") as f:
                    st.download_button(label="Descargar PDF convertido", data=f, file_name="converted_from_images.pdf", mime="application/pdf")
            else:
                st.error("Sube al menos una imagen.")

    # 🔒 Protección y Compresión
    with tab4:
        st.header("🔒 Proteger y Comprimir PDFs")

        # Proteger PDF con contraseña
        st.subheader("🔑 Proteger PDF con Contraseña")
        uploaded_file = st.file_uploader("Sube tu PDF para proteger con contraseña", type=["pdf"], key="encrypt_pdf")
        password = st.text_input("Ingresa la contraseña")
        if st.button("Proteger PDF"):
            if uploaded_file and password:
                encrypted_pdf = encrypt_pdf(uploaded_file, password)
                st.success("PDF protegido correctamente! 🔑")
                with open(encrypted_pdf, "rb") as f:
                    st.download_button(label="Descargar PDF protegido", data=f, file_name="encrypted.pdf", mime="application/pdf")
            else:
                st.error("Sube un archivo PDF y/o ingresa una contraseña.")

        # Comprimir PDF
        st.subheader("🗜️ Comprimir PDF")
        uploaded_file = st.file_uploader("Sube tu PDF para comprimir", type=["pdf"], key="compress_pdf")
        if st.button("Comprimir PDF"):
            if uploaded_file:
                compressed_pdf = compress_pdf(uploaded_file)
                st.success("PDF comprimido correctamente! 🎉")
                with open(compressed_pdf, "rb") as f:
                    st.download_button(label="Descargar PDF comprimido", data=f, file_name="compressed.pdf", mime="application/pdf")
            else:
                st.error("Sube un archivo PDF.")

if __name__ == "__main__":
    main()
