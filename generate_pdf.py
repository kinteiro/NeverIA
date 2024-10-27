from fpdf import FPDF
import io
import re

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Reporte de Recetas', align='C', ln=1)
        self.ln(10)
    
    def add_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, ln=True)
        self.ln(4)
    
    def add_subtitle(self, subtitle):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, subtitle, ln=True)
        self.ln(2)
    
    def add_paragraph(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln(5)
    
    def add_list_item(self, item):
        self.set_font('Arial', '', 12)
        self.cell(5)  # Indent
        self.cell(0, 10, f"- {item}", ln=True)
        

def pass_pdf_to_download(text, imagen=None):
    # Usar expresión regular para eliminar la parte inicial hasta "Ingredientes:"
    match = re.search(r"Ingredientes:", text)
    if match:
        # Retener solo desde "Ingredientes:" hasta el final
        d_text = text[match.start():]
    else:
        # Si no se encuentra el texto, usar el texto completo
        d_text = text.replace("💡", "")
    
    pdf = PDF()
    pdf.add_page()

    # Procesar cada línea para ajustar el formato
    lines = d_text.splitlines()
    for line in lines:
        line = line.strip()

        # Eliminar marcas de Markdown y otros caracteres no deseados
        line = re.sub(r"\*\*", "", line)
        line = re.sub(r"# ", "", line)  
        line = re.sub(r"###", "", line) 
        line = re.sub(r"- ", "", line)  
        line = re.sub(r"##", "", line) 

        # Filtrar líneas vacías o que no contienen información relevante
        if not line or "recetas" in line.lower():
            continue

        if "Ingredientes:" in line:  # Agrega el título de ingredientes
            pdf.add_subtitle("Ingredientes")
        elif line and (line[0].isdigit() and line[1] == "."):  # Instrucciones numeradas
            pdf.add_paragraph(line)
        elif line:  # Normal paragraph text
            pdf.add_paragraph(line.strip())
    
    # Crear un archivo en memoria
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer, 'F')
    pdf_buffer.seek(0)
    
    return pdf_buffer
