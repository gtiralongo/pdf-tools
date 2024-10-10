# PDF Manipulation Tool

## Descripción

Este proyecto es una herramienta completa para manipulación de archivos PDF. La aplicación web, creada con **Streamlit**, permite realizar diversas operaciones como unir, comprimir, dividir, convertir, agregar marcas de agua, reordenar páginas, proteger con contraseña y extraer texto de archivos PDF mediante OCR.

## Funcionalidades

- **Unir PDFs**: Combina múltiples archivos PDF en uno solo.
- **Comprimir PDF**: Reduce el tamaño del archivo PDF.
- **Dividir PDF**: Divide un PDF en varios archivos más pequeños.
- **Convertir PDF a Imágenes**: Convierte cada página del PDF en una imagen.
- **Convertir Imágenes a PDF**: Convierte imágenes en un archivo PDF.
- **Agregar Marca de Agua**: Añade texto como marca de agua en todas las páginas de un PDF.
- **Extraer Texto de PDF (OCR)**: Extrae el texto de un PDF escaneado utilizando OCR.
- **Reordenar Páginas de un PDF**: Cambia el orden de las páginas de un PDF.
- **Proteger PDF con Contraseña**: Protege un PDF con una contraseña.
- **Convertir PDF a Texto (TXT)**: Extrae todo el texto de un PDF y lo guarda en formato de texto plano.

## Instalación

### Requisitos previos

Antes de instalar los requerimientos, asegúrate de tener las siguientes dependencias:

1. **Python**: Versión 3.7 o superior.
2. **Poppler-utils**: Necesario para la conversión de PDF a imágenes.

En sistemas Linux, puedes instalarlo con:
```bash
sudo apt-get install poppler-utils
```

3. **Tesseract OCR**: Necesario para la extracción de texto mediante OCR.

En sistemas Linux, puedes instalarlo con:
```bash
sudo apt-get install tesseract-ocr
```

### Clonar el repositorio

Clona el repositorio del proyecto a tu máquina local:
```bash
git clone https://github.com/tu-usuario/pdf-manipulation-tool.git
cd pdf-manipulation-tool
```

### Instalación de dependencias

Instala los requerimientos de Python necesarios para el proyecto:
```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye las siguientes dependencias:

```txt
streamlit
pytesseract
pdf2image
PyPDF2
Pillow
```

## Uso

### Ejecución de la aplicación

Para ejecutar la aplicación, utiliza el siguiente comando en tu terminal:

```bash
streamlit run app.py
```

Esto abrirá la aplicación web en tu navegador, donde podrás manipular tus archivos PDF.

### Funcionalidades disponibles en la aplicación

1. **Unir PDFs**: Sube múltiples archivos PDF y la aplicación los combinará en uno solo.
2. **Comprimir PDF**: Sube un archivo PDF y la aplicación reducirá su tamaño.
3. **Dividir PDF**: Sube un archivo PDF y define cuántas páginas por archivo deseas.
4. **Convertir PDF a Imágenes**: Sube un archivo PDF y convierte cada página en una imagen (PNG).
5. **Convertir Imágenes a PDF**: Sube varias imágenes y la aplicación las combinará en un archivo PDF.
6. **Agregar Marca de Agua**: Sube un archivo PDF y agrega una marca de agua personalizada.
7. **Extraer Texto (OCR)**: Sube un PDF escaneado y extrae el texto de sus imágenes.
8. **Reordenar Páginas**: Sube un PDF y especifica el nuevo orden de las páginas.
9. **Proteger con Contraseña**: Sube un PDF y establece una contraseña para protegerlo.
10. **Convertir PDF a TXT**: Sube un PDF y extrae todo el texto.

## Configuración adicional

### Configuración de `pytesseract`

Si usas `pytesseract` en sistemas Windows, necesitarás descargar e instalar [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) y asegurarte de agregar la ruta a su ejecutable en el PATH de tu sistema.

Por ejemplo, puedes configurar `pytesseract` en el archivo `app.py` como sigue:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Convertir PDF a Imágenes (Poppler)

En algunos sistemas, también es necesario agregar el binario de `poppler` a tu PATH si estás usando Windows. Descárgalo desde [Poppler](https://github.com/oschwartz10612/poppler-windows).

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras un error o deseas mejorar alguna funcionalidad, no dudes en abrir un _issue_ o enviar un _pull request_.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.

## Créditos

Herramienta desarrollada con **Streamlit**, **PyPDF2**, **pdf2image**, **Pillow**, y **pytesseract**.
