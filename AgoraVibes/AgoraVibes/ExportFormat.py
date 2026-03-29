from import_export.formats.base_formats import Format
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class PDFFormat(Format):
    def get_title(self):
        return "pdf"

    def get_extension(self):
        return "pdf"

    def get_content_type(self):
        return "application/pdf"
    
    def can_import(self):
        return False
        
    def can_export(self):
        return True

    def export_data(self, dataset, **kwargs):
        buffer = BytesIO()
        
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                                rightMargin=20, leftMargin=20,
                                topMargin=20, bottomMargin=20)
        elements = []

        data = []
        if dataset.headers:
            data.append(dataset.headers)
            
        for row in dataset:
            #convierte todos los elementos en strings
            data.append([str(item) if item is not None else '' for item in row])

        if not data:
             data.append(["No hay registros disponibles para exportar."])

        table = Table(data, repeatRows=1)
        
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002B36')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        #alterna el color de la fila
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f0f5f9'))
                
        table.setStyle(style)
        elements.append(table)
        
        doc.build(elements)
        return buffer.getvalue()
