from spire.pdf.common import *
from spire.pdf import *

##############################
InputFile = "c:\\aaa\\PDFs\\Gibly_David.pdf"
OutputFile1 = "c:\\aaa\\PDFs\\Test_1A.doc"
OutputFile2 = "c:\\aaa\\PDFs\\Test_1B.doc"
##############################

# Create an object of the PdfDocument class
doc = PdfDocument()

# Load a PDF document
doc.LoadFromFile(InputFile)

OutputFile1 = "c:\\aaa\\PDFs\\Test_1A.doc"
OutputFile2 = "c:\\aaa\\PDFs\\Test_1B.doc"

# Convert the PDF document to a Word DOCX file
doc.SaveToFile(OutputFile1, FileFormat.DOCX)

# Or convert the PDF document to a Word DOC file
# doc.SaveToFile(OutputFile2, FileFormat.DOC)

# Or convert the PDF document to Text File
doc.SaveToFile(OutputFile2, FileFormat.TEXT)

# Close the PdfDocument object
doc.Close()
